from sqlalchemy.orm import Session
from app.db import models

def get_all_users(db: Session):
    return db.query(models.User).all()

def set_kill_switch(db: Session, user_id: int, status: bool):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return None
    user.kill_switch = status
    db.commit()
    db.refresh(user)
    return user
