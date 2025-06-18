from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 📌 Step 1: Define the database connection URL
# For now, we’re using SQLite, which stores the database in a local file named 'watchlist.db'
# Later, we'll replace this with a PostgreSQL URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./watchlist.db"

# 📌 Step 2: Create the SQLAlchemy engine
# This is what actually communicates with the database
# `check_same_thread=False` is required for SQLite + FastAPI to work
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 📌 Step 3: Create a configured "Session" class
# This lets us create database sessions to run queries
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 📌 Step 4: Create a base class for all your SQLAlchemy models
# You’ll use this to define your tables in models.py
Base = declarative_base()
