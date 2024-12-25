from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from models import ScraperSettings
from scraper import Scraper

# Static Token (You can change this to your desired token)
API_TOKEN = "your_static_token_here"

app = FastAPI()

# Dependency to check for valid token
def verify_token(authorization: str = Header(...)):
    if authorization != f"Bearer {API_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True

@app.post("/scrape/")
async def scrape(settings: ScraperSettings = ScraperSettings(), authorization: str = Depends(verify_token)):
    scraper = Scraper(settings)
    scraper.scrape()
    return {"message": f"Scraped {len(scraper.products)} products and updated DB."}
