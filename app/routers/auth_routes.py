from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.schemas import UserCreate, UserOut
from app.db.crud.user import create_user, get_user_by_username
from app.db.db_setup import get_db
from app.utils.auth import verify_password, create_access_token
from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    return create_user(db, user)


@router.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_username(db, req.username)
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
