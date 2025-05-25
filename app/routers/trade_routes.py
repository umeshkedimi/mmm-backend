from fastapi import APIRouter, Depends
from app.services.kite_service import get_kite
from app.services import trade_manager, pnl_tracker, kill_switch
from app.utils.auth import verify_api_key, get_current_user
from sqlalchemy.orm import Session
from app.db.db_setup import get_db
from app.db import schemas
from app.db.crud.trade_log import create_trade_log
from app.db.models import User

router = APIRouter(prefix="/trade", tags=["Trade"])

@router.get("/ping")
def ping():
    return {"message": "MCP Server is running!"}

@router.get("/user_info")
def get_user(current_user: User = Depends(get_current_user)):
    kite = get_kite()
    return kite.profile()

@router.get("/secure-ping")
def secure_ping(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}, you are authenticated"}

@router.post("/buy")
def buy_order(current_user: User = Depends(get_current_user)):
    return trade_manager.place_order("buy", user=current_user)

@router.post("/sell")
def sell_order(current_user: User = Depends(get_current_user)):
    return trade_manager.place_order("sell", user=current_user)

@router.get("/pnl")
def get_pnl():
    return pnl_tracker.get_pnl()

@router.post("/kill")
def trigger_kill_switch():
    return kill_switch.activate_kill_switch()

@router.post("/log_trade", response_model=schemas.TradeLogOut)
def log_trade(log: schemas.TradeLogCreate, db: Session = Depends(get_db)):
   return create_trade_log(db, log)


