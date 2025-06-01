from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db.models.broker_account import BrokerAccount
from app.schemas.broker_account import BrokerAccountCreate, BrokerAccountUpdate


def get_broker_account_by_user_id(db: Session, user_id: int):
    return db.query(BrokerAccount).filter(BrokerAccount.user_id == user_id).first()


def create_or_update_broker_account(db: Session, user_id: int, data: BrokerAccountCreate):
    existing = get_broker_account_by_user_id(db, user_id)

    if existing:
        for field, value in data.dict().items():
            setattr(existing, field, value)
        db.commit()
        db.refresh(existing)
        return existing
    else:
        new_account = BrokerAccount(user_id=user_id, **data.dict())
        db.add(new_account)
        db.commit()
        db.refresh(new_account)
        return new_account
