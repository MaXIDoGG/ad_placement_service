
from sqlalchemy import Integer, String, ForeignKey, Text, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base
from .user import User

class Review(Base):
    __tablename__ = 'ad'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String, nullable=True)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    image_url: Mapped[str] = mapped_column(String, nullable=True) # Добавить список картинок
    created_at: Mapped[datetime] = mapped_column(DateTime)
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="reviews")
    
    ad_id: Mapped[int] = mapped_column(Integer, ForeignKey('ad.id'))
    ad = relationship("Ad", back_populates="reviews")
    
    
