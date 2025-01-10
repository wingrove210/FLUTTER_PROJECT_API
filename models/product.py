from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    image = Column(String, nullable=True)
    price = Column(Integer, nullable=False)
    is_available = Column(Boolean, default=True)
    stock = Column(Integer, default=0)
