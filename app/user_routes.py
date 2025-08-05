from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app import schemas_users
from app.logging_config import logger

from app import models
from app.auth import (
    get_db, hash_password, authenticate_user,
    create_access_token, get_current_user
)

router = APIRouter()

# User signup
# Create new users with hashed passwords
@router.post("/signup")
def signup(user:schemas_users.UserCreate, db: Session = Depends(get_db)):
# def signup(username: str, email: str, password: str, db: Session = Depends(get_db)):

    logger.info("User signing up.....")

    try:
        # Check if user already exists
        if db.query(models.User).filter(models.User.username == user.username).first():
            logger.info("Username already taken")
            raise HTTPException(status_code=400, detail="Username already taken")
        if db.query(models.User).filter(models.User.email == user.email).first():
            logger.info("Email already registered")
            raise HTTPException(status_code=400, detail="Email already registered")

        new_user = models.User(
            username=user.username,
            email=user.email,
            hashed_password=hash_password(user.password)
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        logger.info(f"Signup attempt for user: {user.username}")
        return {"message": "User created successfully"}
    except Error as er:
        logging.info("Error occured while signuping up: {er}")


# User login
# Verify password, return JWT
@router.post("/login")  
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=30)
    )
    logger.info(f"login attempt for user: {form_data.username}")
    return {"access_token": access_token, "token_type": "bearer"}


# Protected route
@router.get("/me")
def read_users_me(current_user: models.User = Depends(get_current_user)):
    logger.info(f"logined as: {current_user.username}")
    return {
        "username": current_user.username,
        "email": current_user.email
    }
