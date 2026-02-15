from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session, Session
from sqlalchemy import text
from app.database import engine, Base
from app.deps import get_db, get_current_user
from app.models import User
from app.schemas import UserCreate, TokenResponse, UserOut
from app.security import hash_password, verify_password, create_access_token
from app.routers import auth

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/db-test")
def db_test(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1")).scalar()
    return {"db": result}

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.post("/api/auth/register", response_model=UserOut)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == payload.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")

    user = User(username=payload.username, password_hash=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.post("/api/auth/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token(subject=user.username)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/api/auth/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user
