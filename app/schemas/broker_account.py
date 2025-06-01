from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class BrokerAccountBase(BaseModel):
    broker_name: Optional[str] = Field("dhan", example="dhan")
    client_id: str = Field(..., example="DHAN123456")
    access_token: str = Field(..., example="abcxyz123token")
    telegram_chat_id: Optional[str] = Field(None, example="-1001234567890")
    lot_size: int = Field(..., example=15)
    index: str = Field(..., example="banknifty")  # "nifty" or "banknifty"
    direction: str = Field(..., example="sell")  # "buy" or "sell"
    is_active: Optional[bool] = Field(True, example=True)


class BrokerAccountCreate(BrokerAccountBase):
    pass


class BrokerAccountUpdate(BrokerAccountBase):
    pass


class BrokerAccountOut(BrokerAccountBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
