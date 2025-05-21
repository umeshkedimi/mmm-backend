from fastapi import APIRouter, Depends
from services.kite_service import get_kite
from services import trade_manager, pnl_tracker, kill_switch
from utils.auth import verify_api_key

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



