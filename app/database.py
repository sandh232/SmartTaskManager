from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from app.logging_config import logger

# Load environment variables from .env
load_dotenv()

# Get the database URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

logger.info("Connecting with SQLite database")
# Create a database engine
# For SQLite, special connect_args are needed
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)


# SessionLocal is used to interact with the DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
logger.info("session to the database successful")

# Base class for model definitions
Base = declarative_base()