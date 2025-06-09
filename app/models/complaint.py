
from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Complaint(Base):
    __tablename__ = 'complaint'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String, nullable=True)
    image_url: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="complaints", lazy="selectin")
    
    ad_id: Mapped[int] = mapped_column(Integer, ForeignKey('ad.id'))
    ad = relationship("Ad", back_populates="complaints", lazy="selectin")
    
    
