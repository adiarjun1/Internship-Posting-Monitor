from sqlalchemy import Column, Integer, String
from .database import Base

# 📌 Define a SQLAlchemy model for the "watches" table
class Watch(Base):
    __tablename__ = "watches"  # The actual table name in the database

    # 📌 Columns in the table:
    id = Column(Integer, primary_key=True, index=True)  
    # - Primary key: unique ID for each watch entry
    # - Indexed for faster search

    company_name = Column(String, index=True)
    # - Name of the company being watched (e.g., "Amazon")

    url = Column(String, unique=True, index=True)
    # - URL to the job board or careers page being monitored
    # - Marked unique so the same URL can't be added twice

    keywords = Column(String, nullable=True)
    # - Optional field for matching certain job titles (e.g., "SWE", "intern")

    notification_method = Column(String)
    # - How the user wants to be alerted (e.g., "email", "sms")
