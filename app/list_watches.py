from app.database import SessionLocal
from app import crud

def main():
    db = SessionLocal()
    watches = crud.get_watches(db)
    if not watches:
        print("No watches defined.")
    else:
        print("Currently watching:")
        for w in watches:
            print(f" • {w.company_name} → {w.url}")
    db.close()

if __name__ == "__main__":
    main()
