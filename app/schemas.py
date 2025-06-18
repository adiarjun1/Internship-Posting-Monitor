from pydantic import BaseModel
from typing import Optional

# 📌 This schema defines what the client must send to POST /watch
class WatchCreate(BaseModel):
    company_name: str
    url: str
    keywords: Optional[str] = None  # Optional field
    notification_method: str  # e.g., 'email', 'sms'

# 📌 This schema is used when returning a watch from the API
class WatchOut(WatchCreate):
    id: int

    class Config:
        from_attributes = True
        # 📌 orm_mode tells Pydantic to convert from SQLAlchemy model to JSON
