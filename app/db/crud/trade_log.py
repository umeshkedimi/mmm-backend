from sqlalchemy.orm import Session
from app.db import models, schemas

def create_trade_log(db: Session, log: schemas.TradeLogCreate):
    db_log = models.TradeLog(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_all_logs(db: Session, limit: int = 100):
    return db.query(models.TradeLog).order_by(models.TradeLog.timestamp.desc()).limit(limit).all()