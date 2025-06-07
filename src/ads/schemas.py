from pydantic import BaseModel
from datetime import datetime

class AdBase(BaseModel):
    type: str
    name: str
    description: str
    price: float
    image_url: str

class AdCreate(AdBase):
    pass

class Ad(AdBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True
