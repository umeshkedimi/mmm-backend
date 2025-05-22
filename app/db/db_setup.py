from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Load DATABASE_URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models (already defined in models.py — just kept for reference)
Base = declarative_base()

# Dependency for FastAPI routes or services
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
