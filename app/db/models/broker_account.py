# app/db/models/broker_account.py

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.db_setup import Base

class BrokerAccount(Base):
    __tablename__ = "broker_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    broker_name = Column(String, nullable=False)
    client_id = Column(String, nullable=False)
    access_token = Column(String, nullable=False)

    telegram_chat_id = Column(String, nullable=True)
    telegram_bot_token = Column(String, nullable=True)

    lot_size = Column(Integer, nullable=False, default=15)
    index = Column(String, nullable=False)  # "nifty" or "banknifty"
    direction = Column(String, nullable=False) # "buy" or "sell"
    
    stop_loss = Column(Float, nullable=True)
    target = Column(Float, nullable=True)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="broker_accounts")
