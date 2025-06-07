from db.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, Float
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    login = Column(String)
    name = Column(String)
    password_hash = Column(String)
    is_admin = Column(Boolean, default=False)
    is_banned = Column(Boolean, default=False)
    
    ads = relationship("Ad", back_populates="user")