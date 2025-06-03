from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BrokerAccountBase(BaseModel):
    broker_name: str
    client_id: str
    access_token: str
    telegram_chat_id: Optional[str]
    telegram_bot_token: Optional[str]
    lot_size: int
    index: str  # "nifty" or "banknifty"
    direction: str  # "buy" or "sell"
    stop_loss: Optional[float]
    target: Optional[float]
    is_active: bool = True

class BrokerAccountCreate(BrokerAccountBase):
    pass

class BrokerAccountUpdate(BaseModel):
    telegram_chat_id: Optional[str]
    telegram_bot_token: Optional[str]
    access_token: Optional[str]
    lot_size: Optional[int]
    direction: Optional[str]
    stop_loss: Optional[float]
    target: Optional[float]
    is_active: Optional[bool]

class BrokerAccountOut(BrokerAccountBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
