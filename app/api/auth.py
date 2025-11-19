from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import base as db_base
from app.db import models
from app.schemas.auth import UserCreate, Token
from app.utils import security

router = APIRouter()

@router.post("/signup", status_code=201)
def signup(payload: UserCreate, db: Session = Depends(db_base.get_db)):
    u = db.query(models.User).filter(models.User.email == payload.email).first()
    if u:
        raise HTTPException(400, "Email already registered")
    user = models.User(email=payload.email, hashed_password=security.hash_password(payload.password), is_admin=True)
    db.add(user); db.commit(); db.refresh(user)
    return {"msg": "user created"}

@router.post("/login", response_model=Token)
def login(payload: UserCreate, db: Session = Depends(db_base.get_db)):
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if not user or not security.verify_password(payload.password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")
    token = security.create_access_token(subject=user.id)
    return {"access_token": token, "token_type": "bearer"}
