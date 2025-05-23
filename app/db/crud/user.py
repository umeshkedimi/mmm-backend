from sqlalchemy.orm import Session
from app.db import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = pwd_context.hash(user.password)
    db_user = models.User(
        username=user.username,
        hashed_password=hashed_pw,
        broker=user.broker,
        api_key=user.api_key,
        api_secret=user.api_secret,
        totp_secret=user.totp_secret
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
