import asyncio
from playwright.async_api import async_playwright
from sqlalchemy.orm import Session
from app import models, database, crud
from datetime import timezone, datetime

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

async def scrape():
    db: Session = database.SessionLocal()
    watch = db.query(models.Watch).first()
    if not watch:
        print("No watch targets found.")
        return

    print(f"Scraping jobs for {watch.company_name} from {watch.url}...")
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(watch.url, wait_until="domcontentloaded")
        await page.wait_for_selector("div.job-tile", timeout=15000)

        job_tiles = await page.query_selector_all("div.job-tile h3.job-title a")

        new_jobs = []
        for jt in job_tiles:
            title = (await jt.inner_text()).strip()
            href = await jt.get_attribute("href")
            full_url = "https://www.amazon.jobs" + href

            # Extract Amazon’s internal job-id from the URL (e.g., ".../jobs/2825134/...")
            job_id = href.split("/jobs/")[1].split("/")[0]

            # Delta detection: skip if already exists
            if crud.job_exists(db, watch.id, job_id):
                continue

            # Otherwise, persist and note it as new
            created = crud.create_job(db, watch.id, job_id, title, full_url)
            new_jobs.append(created)

        await browser.close()

    if not new_jobs:
        print("No new jobs found.")
    else:
        print(f"🎉 Found {len(new_jobs)} new job(s):\n")
        for job in new_jobs:
            print(f"- {job.title}\n  ↳ {job.url}")

        send_email_alert(new_jobs, watch)

def send_email_alert(jobs, watch):
    """
    Send an email listing all new jobs for a given Watch,
    with debug prints of environment variables and any errors.
    """
    if not jobs:
        print("No new jobs to email.")
        return

    # 🔍 Debug: print out the env vars we’re using
    print("DEBUG: SENDGRID_API_KEY =", os.environ.get("SENDGRID_API_KEY"))
    print("DEBUG: SENDGRID_FROM_EMAIL =", os.environ.get("SENDGRID_FROM_EMAIL"))
    print("DEBUG: ALERT_EMAIL =", os.environ.get("ALERT_EMAIL"))

    subject = f"[JobWatcher] {len(jobs)} new {watch.company_name} internships"
    lines = [f"{job.title}\n{job.url}" for job in jobs]
    content = "\n\n".join(lines)

    message = Mail(
        from_email=os.environ.get("SENDGRID_FROM_EMAIL", ""),
        to_emails=os.environ.get("ALERT_EMAIL", ""),
        subject=subject,
        plain_text_content=content
    )
    try:
        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY", ""))
        response = sg.send(message)
        print(f"Email sent with status code {response.status_code}")
        # 🔍 Debug: print response body if non-2xx
        if response.status_code >= 300:
            print("DEBUG: response body:", response.body if hasattr(response, 'body') else "<no body>")
    except Exception as e:
        print("❌ Failed to send email:", repr(e))

if __name__ == "__main__":
    asyncio.run(scrape())
