from pydantic import BaseModel, Field
from datetime import datetime

from models import AdType

class AdBase(BaseModel):
    type: AdType = Field(default=AdType.SALE)
    name: str
    description: str
    price: float
    image_url: str

    class Config:
        use_enum_values = True
        from_attributes = True


class AdCreate(AdBase):
    pass

class Ad(AdBase):
    id: int
    user_id: int
    created_at: datetime

class ReviewBase(BaseModel):
    text: str
    rating: int = Field(..., ge=1, le=5)
    image_url: str | None = None
    
class ReviewCreate(ReviewBase):
    pass

    
class Review(ReviewBase):
    id: int
    ad_id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
        

class ComplaintBase(BaseModel):
    text: str
    image_url: str | None = None
    
class ComplaintCreate(ComplaintBase):
    pass

    
class Complaint(ComplaintBase):
    id: int
    ad_id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True