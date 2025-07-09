import os
from celery import Celery

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "jobwatcher",
    broker=CELERY_BROKER_URL,
    include=["app.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

celery_app.conf.beat_schedule = {
    "scrape-every-5-minutes": {
        "task": "app.tasks.run_scraper",
        "schedule": 300.0,
    },
}
