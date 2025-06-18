# app/scraper.py

import asyncio
from playwright.async_api import async_playwright
from sqlalchemy.orm import Session
from app import models, database

async def scrape():
    # 📌 Step 1: Open DB session and grab your first watch
    db: Session = database.SessionLocal()
    watch = db.query(models.Watch).first()
    if not watch:
        print("No watch targets found.")
        return

    print(f"Scraping jobs for {watch.company_name} from {watch.url}...")

    # 📌 Step 2: Launch headless Chromium
    async with async_playwright() as p:
        browser = await p.chromium.launch()            # headless by default
        page = await browser.new_page()
        await page.goto(watch.url, wait_until="domcontentloaded")

        # Step 3: Now wait for the job tiles to render in the DOM
        # This will poll until at least one .job-tile exists (max 15 s)
        await page.wait_for_selector("div.job-tile", timeout=15000)

        # 📌 Step 4: Extract titles and links
        job_tiles = await page.query_selector_all("div.job-tile h3.job-title a")
        print(f"Found {len(job_tiles)} job(s):\n")
        for jt in job_tiles:
            title = (await jt.inner_text()).strip()
            href = await jt.get_attribute("href")
            link = "https://www.amazon.jobs" + href
            print(f"- {title}\n  ↳ {link}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape())
