from db.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, Float
from sqlalchemy.orm import relationship

class Ad(Base):
    __tablename__ = 'ad'
    
    id = Column(Integer, primary_key=True)
    type = Column(String, default="Продажа") # В будущем добавить Enum
    name = Column(String)
    description = Column(Text)
    price = Column(Float)
    image = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))
    
    user = relationship("User", back_populates="ads")
