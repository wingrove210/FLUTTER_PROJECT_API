from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    image: Optional[str] = None
    price: float
    is_available: bool = True
    stock: int = 0

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None

class ProductResponse(ProductBase):
    id: int

    class Config:
        orm_mode = True
