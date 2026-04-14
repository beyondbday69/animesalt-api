from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from scraper import scrape_home, scrape_search, scrape_details, scrape_episode

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = FastAPI(
    title="AnimeSalt API",
    description="An unofficial scraper API for animesalt.ac",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    logging.error(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"},
    )

@app.get("/")
async def root():
    return {"message": "Welcome to the AnimeSalt API. Visit /docs for documentation."}

@app.get("/api/home")
async def get_home(response: Response):
    """Scrape latest anime, trending, and featured sections."""
    # Cache on CDN for 1 hour, stale while revalidate for 24 hours
    response.headers["Cache-Control"] = "public, s-maxage=3600, stale-while-revalidate=86400"
    data = await scrape_home()
    return {"success": True, "data": data}

@app.get("/api/search")
async def get_search(response: Response, q: str = Query(..., description="Search query")):
    """Scrape search results dynamically."""
    # Cache searches for 1 hour
    response.headers["Cache-Control"] = "public, s-maxage=3600, stale-while-revalidate=86400"
    data = await scrape_search(q)
    return {"success": True, "query": q, "results": data}

@app.get("/api/anime/{slug}")
async def get_anime_details(response: Response, slug: str):
    """Scrape Title, Description, Genres, Episodes list, Thumbnail."""
    # Cache details for 12 hours
    response.headers["Cache-Control"] = "public, s-maxage=43200, stale-while-revalidate=86400"
    data = await scrape_details(slug)
    return {"success": True, "data": data}

@app.get("/api/episode/{episode_id}")
async def get_episode(response: Response, episode_id: str):
    """Extract video player or iframe. If m3u8 link exists, return it."""
    # Cache episode links for 24 hours (links rarely change)
    response.headers["Cache-Control"] = "public, s-maxage=86400, stale-while-revalidate=86400"
    data = await scrape_episode(episode_id)
    return {"success": True, "data": data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=500, reload=True)
