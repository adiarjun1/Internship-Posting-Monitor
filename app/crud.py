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
