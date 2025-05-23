from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.schemas import UserCreate, UserOut
from app.db.crud.user import create_user, get_user_by_username
from app.db.db_setup import get_db

router = APIRouter()

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    return create_user(db, user)
