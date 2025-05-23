from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TradeLogCreate(BaseModel):
    symbol: str
    direction: str  # e.g. "buy" or "sell"
    quantity: int
    price: float
    pnl: Optional[float] = None
    exit_reason: Optional[str] = None  # e.g. "stop_loss", "take_profit", "manual_exit"

class TradeLogOut(TradeLogCreate):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username: str
    password: str
    broker: str
    api_key: str
    api_secret: str
    totp_secret: str

class UserOut(BaseModel):
    id: int
    username: str
    broker: str

    class Config:
        orm_mode = True