from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from . import models, schemas, crud
from .database import SessionLocal, engine, Base

# 📌 Create the database tables (if they don't exist yet)
Base.metadata.create_all(bind=engine)

# 📌 Initialize FastAPI app
app = FastAPI()

# 📌 Dependency that gives us a DB session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db  # provides db session to route function
    finally:
        db.close()  # always close after request is done

# 📌 POST /watch — add a new job URL to watch
@app.post("/watch", response_model=schemas.WatchOut)
def add_watch(watch: schemas.WatchCreate, db: Session = Depends(get_db)):
    return crud.create_watch(db, watch)

# 📌 GET /watch — get all watched job URLs
@app.get("/watch", response_model=list[schemas.WatchOut])
def read_watches(db: Session = Depends(get_db)):
    return crud.get_watches(db)

# 📌 DELETE /watch/{watch_id} — delete a specific watch
@app.delete("/watch/{watch_id}")
def delete_watch(watch_id: int, db: Session = Depends(get_db)):
    crud.delete_watch(db, watch_id)
    return {"message": "Deleted"}
