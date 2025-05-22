from fastapi import APIRouter, Depends
from app.services.kite_service import get_kite
from app.services import trade_manager, pnl_tracker, kill_switch
from app.utils.auth import verify_api_key
from sqlalchemy.orm import Session
from app.db.db_setup import get_db
from app.db import schemas
from app.db.crud.trade_log import create_trade_log

router = APIRouter(prefix="/trade", tags=["Trade"])

@router.get("/ping")
def ping():
    return {"message": "MCP Server is running!"}

@router.get("/user_info")
def get_user():
    kite = get_kite()
    return kite.profile()

@router.post("/buy", dependencies=[Depends(verify_api_key)])
def buy_order():
    return trade_manager.place_order("buy")

@router.post("/sell", dependencies=[Depends(verify_api_key)])
def sell_order():
    return trade_manager.place_order("sell")

@router.get("/pnl")
def get_pnl():
    return pnl_tracker.get_pnl()

@router.post("/kill", dependencies=[Depends(verify_api_key)])
def trigger_kill_switch():
    return kill_switch.activate_kill_switch()

@router.post("/log_trade", response_model=schemas.TradeLogOut)
def log_trade(log: schemas.TradeLogCreate, db: Session = Depends(get_db)):
   return create_trade_log(db, log)


