import asyncio
from bs4 import BeautifulSoup
from curl_cffi.requests import AsyncSession
from fastapi import HTTPException
import logging
from async_lru import alru_cache

BASE_URL = "https://animesalt.ac"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": BASE_URL + "/"
}

logger = logging.getLogger(__name__)

async def fetch_page(url: str):
    try:
        async with AsyncSession(impersonate="chrome120") as session:
            response = await session.get(url, headers=HEADERS, timeout=15)
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail="Page not found")
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Failed to fetch page")
            return response.text
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        logger.error(f"Error fetching {url}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def fetch_season_html(post_id: str, season_num: str, referer: str):
    url = f"{BASE_URL}/wp-admin/admin-ajax.php?action=action_select_season&season={season_num}&post={post_id}"
    try:
        async with AsyncSession(impersonate="chrome120") as session:
            r = await session.get(url, headers={"User-Agent": HEADERS["User-Agent"], "Referer": referer}, timeout=15)
            if r.status_code == 200:
                return season_num, r.text
    except Exception as e:
        logger.error(f"Error fetching season {season_num}: {e}")
    return season_num, ""

def _extract_image(img_tag):
    if not img_tag:
        return None
    # Check data-src first (lazy loading), then src
    src = img_tag.get('data-src') or img_tag.get('src')
    if src and src.startswith('//'):
        src = 'https:' + src
    return src

def _extract_anime_list(soup, selector):
    animes = []
    items = soup.select(selector)
    for item in items:
        title_elem = item.select_one("h2, h3, .title, .entry-title")
        link_elem = item.select_one("a.lnk-blk")
        img_elem = item.select_one("img")
        
        if link_elem and link_elem.get("href"):
            title = title_elem.text.strip() if title_elem else ""
            if not title and img_elem and img_elem.get("alt"):
                title = img_elem.get("alt").replace("Image ", "").strip()
                
            animes.append({
                "title": title,
                "url": link_elem["href"],
                "slug": link_elem["href"].strip("/").split("/")[-1],
                "image": _extract_image(img_elem)
            })
    return animes

def _extract_episodes(soup_or_html, season_num=None):
    if isinstance(soup_or_html, str):
        soup = BeautifulSoup(soup_or_html, "lxml")
    else:
        soup = soup_or_html
        
    episodes = []
    ep_items = soup.select("article.episodes")
    for item in ep_items:
        ep_num = item.select_one(".num-epi")
        ep_title = item.select_one(".entry-title")
        ep_link = item.parent.select_one("a.lnk-blk") or item.select_one("a.lnk-blk")
        img_elem = item.select_one("img")
        
        ep_url = ep_link["href"] if ep_link else ""
        
        ep_data = {
            "number": ep_num.text.strip() if ep_num else "",
            "title": ep_title.text.strip() if ep_title else "",
            "url": ep_url,
            "id": ep_url.strip("/").split("/")[-1] if ep_url else "",
            "thumbnail": _extract_image(img_elem)
        }
        if season_num is not None:
            ep_data["season"] = season_num
            
        episodes.append(ep_data)
    return episodes

@alru_cache(maxsize=32)
async def scrape_home():
    html = await fetch_page(BASE_URL)
    soup = BeautifulSoup(html, "lxml")
    
    result = {}
    
    sections = soup.select("section")
    for section in sections:
        header = section.select_one("h2, h3, .title, .section-title")
        if header:
            section_name = header.text.strip()
            if not section_name:
                continue
                
            key = section_name.lower().replace(" ", "_").replace("»", "").strip("_")
            animes = _extract_anime_list(section, "article.post, .item, .post")
            
            if animes:
                result[key] = animes
    
    return result

@alru_cache(maxsize=128)
async def scrape_search(query: str):
    url = f"{BASE_URL}/?s={query}"
    html = await fetch_page(url)
    soup = BeautifulSoup(html, "lxml")
    
    return _extract_anime_list(soup, "article.post")

@alru_cache(maxsize=256)
async def scrape_details(slug: str):
    url = f"{BASE_URL}/series/{slug}/"
    is_movie = False
    html = ""
    try:
        html = await fetch_page(url)
    except HTTPException as e:
        if e.status_code == 404:
            try:
                url = f"{BASE_URL}/movies/{slug}/"
                html = await fetch_page(url)
                is_movie = True
            except Exception:
                raise HTTPException(status_code=404, detail="Anime/Movie not found")
        else:
            raise e
            
    soup = BeautifulSoup(html, "lxml")
    
    title_elem = soup.select_one("h1")
    title = title_elem.text.strip() if title_elem else ""
    
    desc_elem = soup.select_one("#overview-text p")
    description = desc_elem.text.strip() if desc_elem else ""
    
    genres = []
    genre_headers = soup.select("h4")
    for header in genre_headers:
        if "Genres" in header.text:
            genre_links = header.parent.select("a")
            genres = [g.text.strip() for g in genre_links]
            break
            
    thumbnail_elem = soup.select_one(".bd > div:first-child img")
    thumbnail = _extract_image(thumbnail_elem)
    
    episodes = []
    movie_players = []
    
    if is_movie:
        # Movies typically have iframes directly on the page instead of episodes
        iframes = soup.select("iframe")
        for iframe in iframes:
            src = iframe.get('data-src') or iframe.get('src')
            if src and "animesalt.ac" not in src and "youtube.com" not in src:
                movie_players.append(src)
        
        # Sometimes movies are split into parts and act like episodes
        episodes = _extract_episodes(soup, "1")
    else:
        # Series
        season_btns = soup.select(".season-btn")
        if season_btns:
            post_id = season_btns[0].get("data-post")
            season_nums = [btn.get("data-season") for btn in season_btns]
            
            tasks = [fetch_season_html(post_id, s, url) for s in season_nums]
            results = await asyncio.gather(*tasks)
            
            # To keep them ordered, we could sort by season_num
            # or just append them as they complete if we use a dict
            episodes_dict = {}
            for s_num, s_html in results:
                if s_html:
                    episodes_dict[s_num] = _extract_episodes(s_html, s_num)
            
            # Flatten into a single list ordered by season
            for s_num in sorted(episodes_dict.keys(), key=lambda x: int(x) if x.isdigit() else x):
                episodes.extend(episodes_dict[s_num])
        else:
            # Single season or no season buttons found
            episodes = _extract_episodes(soup, "1")
        
    return {
        "title": title,
        "description": description,
        "genres": genres,
        "thumbnail": thumbnail,
        "is_movie": is_movie,
        "episodes": episodes,
        "movie_players": movie_players
    }

@alru_cache(maxsize=512)
async def scrape_episode(episode_id: str):
    url = f"{BASE_URL}/episode/{episode_id}/"
    html = await fetch_page(url)
    soup = BeautifulSoup(html, "lxml")
    
    iframe = soup.select_one("iframe")
    video_url = iframe["src"] if iframe else None
    
    # Check if there is an m3u8 directly available
    m3u8_link = None
    if video_url and "m3u8" in video_url:
        m3u8_link = video_url

    prev_episode_id = None
    next_episode_id = None
    for a in soup.find_all("a", href=True):
        html_str = str(a)
        if "19 20 9 12 19 4 19 20" in html_str:
            prev_episode_id = a["href"].strip("/").split("/")[-1]
        elif "5 4 15 12 5 20 5 4" in html_str:
            next_episode_id = a["href"].strip("/").split("/")[-1]
        
    return {
        "video_player": video_url,
        "m3u8_link": m3u8_link,
        "source": url,
        "next_episode_id": next_episode_id,
        "prev_episode_id": prev_episode_id
    }