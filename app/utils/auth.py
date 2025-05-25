import os
from fastapi import Request, HTTPException, status, Depends
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from app.db.db_setup import get_db
from app.db.crud.user import get_user_by_username
from sqlalchemy.orm import Session

API_KEY = os.getenv("API_KEY_HEADER")

def verify_api_key(request: Request):
    header_key = request.headers.get("X-API-KEY")
    if not header_key or header_key != API_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized access")
    


SECRET_KEY = os.getenv("JWT_SECRET", "supersecret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def hash_password(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    username = decode_token(token)  # verifies & extracts 'sub'
    user = get_user_by_username(db, username)
    print("✅ Authenticated user:", user.username, "| Broker:", user.broker)
    print("🔐 Incoming token:", token)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid token user")
    return user