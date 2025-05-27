from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.db_setup import get_db
from app.db import models
from app.db.schemas import UserAdminOut
from app.db.schemas import TradeLogOut
from app.services import user_service, trade_service
from app.utils.auth import get_current_user
from pydantic import BaseModel

router = APIRouter(
    prefix="/admin",
    tags=["Admin Panel"]
)


# --- Helper to verify admin access ---
def ensure_admin(user: models.User):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")


# --- 1. Get All Users ---
@router.get("/users", response_model=List[UserAdminOut])
def get_all_users(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    ensure_admin(current_user)
    return user_service.get_all_users(db)


# --- 2. Get All Trades ---
@router.get("/trades", response_model=List[TradeLogOut])
def get_all_trades(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    ensure_admin(current_user)
    return trade_service.get_all_trades(db)


# --- 3. Kill Switch Toggle ---
class KillSwitchRequest(BaseModel):
    user_id: int
    status: bool


@router.post("/killswitch")
def toggle_kill_switch(
    request: KillSwitchRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    ensure_admin(current_user)
    updated = user_service.set_kill_switch(db, request.user_id, request.status)
    return {"status": "success", "user_id": updated.id, "kill_switch": updated.kill_switch}


# --- 4. Get System Metrics ---
@router.get("/metrics")
def get_admin_metrics(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    ensure_admin(current_user)

    total_users = db.query(models.User).count()
    total_trades = db.query(models.TradeLog).count()
    active_users = db.query(models.User).filter(models.User.kill_switch == False).count()

    return {
        "total_users": total_users,
        "active_users": active_users,
        "total_trades": total_trades
    }
