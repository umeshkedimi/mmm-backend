# app/services/trade_service.py

from sqlalchemy.orm import Session
from app.db.models import TradeLog

def get_all_trades(db: Session):
    return db.query(TradeLog).order_by(TradeLog.timestamp.desc()).all()
