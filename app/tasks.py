# app/tasks.py

from app.celery_app import celery_app    # absolute import
import asyncio
from app.scraper import scrape           # absolute import

@celery_app.task(name="app.tasks.run_scraper")
def run_scraper():
    asyncio.run(scrape())
