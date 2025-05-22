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