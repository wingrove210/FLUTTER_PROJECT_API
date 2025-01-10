from fastapi import FastAPI, HTTPException, Depends, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models.user import User
from database import SessionLocal
from fastapi import APIRouter
from pydantic import BaseModel

auth_router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCreate(BaseModel):
    username: str
    password: str
    
class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper functions
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, username: str, password: str):
    hashed_password = pwd_context.hash(password)  # Hash the password
    new_user = User(username=username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Routes
@auth_router.post("/register", response_model=dict)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Create a new user
    new_user = create_user(db, user.username, user.password)
    
    return {"message": "User  registered successfully"}

@auth_router.get("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=username)
    if not db_user or not verify_password(password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    return {"message": "Login successful"}

@auth_router.get("/users/", response_model=list[UserOut])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@auth_router.get("/logout")
def logout(response: Response):
    response.delete_cookie(key="username")
    return {"message": "Logout successful"}

@auth_router.get("/profile")
def profile(request: Request):
    username = request.cookies.get("username")
    if not username:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return {"username": username}

@auth_router.put("/profile")
def update_profile(username: str, new_password: str, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User  not found")

    # Update the user's password
    db_user.hashed_password = pwd_context.hash(new_password)
    db.commit()
    return {"message": "Profile updated successfully"}