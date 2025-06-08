from pydantic import BaseModel, Field
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
        from_attributes = True

class ReviewBase(BaseModel):
    text: str
    rating: int = Field(..., ge=1, le=5)
    image_url: str | None = None
    ad_id: int

    
class Review(ReviewBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True