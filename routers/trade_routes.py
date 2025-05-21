from fastapi import APIRouter
from services.kite_service import get_kite
from services import trade_manager
from services import pnl_tracker
from services import kill_switch

router = APIRouter(prefix="/trade", tags=["Trade"])

@router.get("/ping")
def ping():
    return {"message": "MCP Server is running!"}

@router.get("/user_info")
def get_user():
    kite = get_kite()
    return kite.profile()

@router.post("/buy")
def buy_order():
    return trade_manager.place_order("buy")

@router.post("/sell")
def sell_order():
    return trade_manager.place_order("sell")

@router.get("/pnl")
def get_pnl():
    return pnl_tracker.get_pnl()

@router.post("/kill")
def trigger_kill_switch():
    return kill_switch.activate_kill_switch()



