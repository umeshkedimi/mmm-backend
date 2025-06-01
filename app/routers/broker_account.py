from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.db_setup import get_db
from app.schemas.broker_account import BrokerAccountCreate, BrokerAccountOut
from app.db.crud.broker_account import get_broker_account_by_user_id, create_or_update_broker_account
from app.utils.auth import get_current_user
from app.db.models.user import User

router = APIRouter(
    prefix="/broker-account",
    tags=["Broker Account"]
)


@router.get("/me", response_model=BrokerAccountOut)
def get_my_broker_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    account = get_broker_account_by_user_id(db, user_id=current_user.id)
    if not account:
        raise HTTPException(status_code=404, detail="Broker account not found.")
    return account


@router.post("/", response_model=BrokerAccountOut)
def create_or_update_my_broker_account(
    data: BrokerAccountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_or_update_broker_account(db, user_id=current_user.id, data=data)
