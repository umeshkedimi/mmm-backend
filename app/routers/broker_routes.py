from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.schemas import BrokerAccountCreate, BrokerAccountOut
from app.utils.auth import get_current_user
from app.db.db_setup import get_db
from app.db.crud import broker_account
from app.db.models import User

router = APIRouter()

@router.post("/broker-account", response_model=BrokerAccountOut)
def add_broker_account(
    account: BrokerAccountCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return broker_account.create_broker_account(db, current_user.id, account)

@router.get("/broker-accounts", response_model=list[BrokerAccountOut])
def list_accounts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return broker_account.get_all_accounts_for_user(db, current_user.id)
