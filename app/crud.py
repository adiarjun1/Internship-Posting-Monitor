from sqlalchemy.orm import Session
from . import models, schemas

# 📌 Create a new Watch entry in the database
def create_watch(db: Session, watch: schemas.WatchCreate):
    # Convert the input Pydantic object into a database object
    db_watch = models.Watch(**watch.dict())
    db.add(db_watch)        # Add to session
    db.commit()             # Commit (save) to DB
    db.refresh(db_watch)    # Refresh to get DB-generated fields like `id`
    return db_watch

# 📌 Get all Watch entries
def get_watches(db: Session):
    return db.query(models.Watch).all()

# 📌 Delete a Watch entry by ID
def delete_watch(db: Session, watch_id: int):
    watch = db.query(models.Watch).get(watch_id)
    if watch:
        db.delete(watch)
        db.commit()

def job_exists(db: Session, watch_id: int, job_id: str) -> bool:
    return (
        db.query(models.Job)
        .filter(models.Job.watch_id == watch_id, models.Job.job_id == job_id)
        .first()
        is not None
    )

# 📌 Create a new Job record
def create_job(
    db: Session,
    watch_id: int,
    job_id: str,
    title: str,
    url: str
) -> models.Job:
    db_job = models.Job(
        watch_id=watch_id,
        job_id=job_id,
        title=title,
        url=url
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

# 📌 Get all stored job_ids for a given watch (optional helper)
def get_job_ids_for_watch(db: Session, watch_id: int) -> list[str]:
    rows = (
        db.query(models.Job.job_id)
        .filter(models.Job.watch_id == watch_id)
        .all()
    )
    # rows is list of tuples, e.g. [("123",), ("456",)]
    return [row[0] for row in rows]