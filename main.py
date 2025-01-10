from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from crud.product import (
    create_product, get_products, get_product, update_product, delete_product
)
from schemas.product import ProductCreate, ProductUpdate, ProductResponse
from fastapi.middleware.cors import CORSMiddleware
from routers.auth_router import auth_router
from routers.product_router import product_router

# Инициализация базы данных
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Регистрируем роутер
app.include_router(auth_router, prefix="/users", tags=["users"])
app.include_router(product_router, prefix="/products", tags=["products"])

origins = [
    "http://localhost:3000",  # Для работы с фронтендом
    "http://localhost:8000",  # Для разработки
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все домены (только для разработки)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Зависимость для получения сессии базы данных
