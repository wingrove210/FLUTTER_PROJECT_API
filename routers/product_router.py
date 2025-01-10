from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from crud.product import (
    create_product, get_products, get_product, update_product, delete_product
)
from schemas.product import ProductCreate, ProductUpdate, ProductResponse
from fastapi.middleware.cors import CORSMiddleware
product_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@product_router.post("/", response_model=ProductResponse)
def create_new_product(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, product)

@product_router.get("/", response_model=list[ProductResponse])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_products(db, skip=skip, limit=limit)

@product_router.get("/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@product_router.put("/{product_id}", response_model=ProductResponse)
def update_existing_product(
    product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)
):
    updated_product = update_product(db, product_id, product_update)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@product_router.delete("/{product_id}", response_model=ProductResponse)
def delete_existing_product(product_id: int, db: Session = Depends(get_db)):
    deleted_product = delete_product(db, product_id)
    if not deleted_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return deleted_product