from sqlalchemy import Column, Integer, String, Float, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TradeLog(Base):
    __tablename__ = "trade_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    symbol = Column(String, nullable=False)
    direction = Column(String, nullable=False) # e.g. "buy" or "sell"
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    pnl = Column(Float, nullable=False)
    exit_reason = Column(String, nullable=True) # e.g. "stop_loss", "take_profit", "manual_exit"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    broker = Column(String, nullable=False)  # "zerodha" or "dhan"
    api_key = Column(String, nullable=True)
    api_secret = Column(String, nullable=True)
    totp_secret = Column(String, nullable=True)