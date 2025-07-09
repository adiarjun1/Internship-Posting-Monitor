from pydantic import BaseModel
from typing import Optional

# What the client must send to POST /watch
class WatchCreate(BaseModel):
    company_name: str
    url: str
    keywords: Optional[str] = None 
    notification_method: str

# When returning a watch from the API
class WatchOut(WatchCreate):
    id: int

    class Config:
        from_attributes = True
