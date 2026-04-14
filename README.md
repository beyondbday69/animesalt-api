# AnimeSalt API

Unofficial scraper API for animesalt.ac.

## Base URL
Production: `https://animesalt-api-lovat.vercel.app`

## Routes

### 1. Home
- **Endpoint:** `GET /api/home`
- **Description:** Scrape latest anime, trending, and featured sections.
- **Cache:** 1 hour

### 2. Search
- **Endpoint:** `GET /api/search?q={query}`
- **Description:** Scrape search results dynamically.
- **Parameters:** `q` (string) - Search term.
- **Cache:** 1 hour

### 3. Anime Details
- **Endpoint:** `GET /api/anime/{slug}`
- **Description:** Scrape Title, Description, Genres, Episodes list, Thumbnail, and Movie Players (if movie).
- **Parameters:** `slug` (string) - Anime slug (e.g., `naruto`).
- **Cache:** 12 hours

### 4. Episode Details
- **Endpoint:** `GET /api/episode/{episode_id}`
- **Description:** Extract video player (iframe) and direct m3u8 link (if available). Also returns `next_episode_id` and `prev_episode_id` for navigation.
- **Parameters:** `episode_id` (string) - Episode ID (e.g., `naruto-1x1`).
- **Cache:** 24 hours

## Auto-Next Logic (Frontend)

If using the iframe (`video_player`):
```javascript
window.addEventListener("message", (e) => {
    if (e.data === "video_playback_completed") {
        // Fetch next_episode_id from API response and load
    }
});
```

To auto-skip intro/outro in iframe:
```javascript
setInterval(() => {
    const iframe = document.querySelector("iframe");
    if (iframe) {
        iframe.contentWindow.postMessage({ autoSkip: { intro: true, outro: true } }, '*');
    }
}, 1000);
```