
from sqlalchemy import Integer, String, ForeignKey, Text, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base
from .user import User

class Ad(Base):
    __tablename__ = 'ad'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String, default="Продажа") # В будущем добавить Enum
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Float)
    image_url: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
    
    user = relationship("User", back_populates="ads")
    reviews = relationship("Review", back_populates="ad")
