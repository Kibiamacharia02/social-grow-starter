from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PostCreate(BaseModel):
    account_id: int
    content: str
    media_url: str
    scheduled_at: datetime

class PostOut(BaseModel):
    id: int
    account_id: int
    content: str
    media_url: str
    scheduled_at: datetime
    status: str
    published_at: Optional[datetime]
    class Config:
        orm_mode = True
