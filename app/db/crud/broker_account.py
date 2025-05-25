from app.db import models, schemas
from sqlalchemy.orm import Session

def get_account_by_broker(db: Session, user_id: int, broker: str):
    return db.query(models.BrokerAccount).filter_by(user_id=user_id, broker=broker).first()

def get_all_accounts_for_user(db: Session, user_id: int):
    return db.query(models.BrokerAccount).filter_by(user_id=user_id).all()

def create_broker_account(db: Session, user_id: int, account: schemas.BrokerAccountCreate):
    new_account = models.BrokerAccount(
        user_id=user_id,
        broker=account.broker,
        api_key=account.api_key,
        api_secret=account.api_secret,
        totp_secret=account.totp_secret
    )
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account
