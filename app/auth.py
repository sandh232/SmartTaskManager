from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

from app import models
from app.database import SessionLocal


# Load environment variables
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# For hashing passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2PasswordBearer expects a token sent in the header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Get DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Password hashing
def hash_password(password: str):
    return pwd_context.hash(password)

# Password verification
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Authenticate user (called during login)
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

# Generate JWT token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Get current user from token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Find user in DB
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user



