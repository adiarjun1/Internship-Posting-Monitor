from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime, timezone
from .database import Base

class Watch(Base):
    __tablename__ = "watches"
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, index=True)
    url = Column(String, unique=True, index=True)
    keywords = Column(String, nullable=True)
    notification_method = Column(String)

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    watch_id = Column(Integer, ForeignKey("watches.id"), index=True)
    job_id = Column(String, index=True)
    title = Column(String)
    url = Column(String)
    scraped_at = Column(DateTime(timezone=True),default=lambda: datetime.now(timezone.utc))
