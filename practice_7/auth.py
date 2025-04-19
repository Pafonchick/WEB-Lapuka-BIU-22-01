from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from models import User
from database import SessionLocal

# Если python-jose не устанавливается, используем pyjwt как альтернативу
try:
    from jose import JWTError, jwt
except ImportError:
    import jwt
    class JWTError(Exception):
        pass

# Настройки для JWT
SECRET_KEY = "your-secret-key-here-please-change-it"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return pwd_context.hash(password)

def authenticate_user(db: Session, login: str, password: str):
    user = db.query(User).filter(User.login == login).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # Работаем с разными библиотеками
    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    except AttributeError:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM).decode('utf-8')

    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(SessionLocal)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        login: str = payload.get("sub")
        if login is None:
            raise credentials_exception
    except (JWTError, Exception) as e:
        raise credentials_exception

    user = db.query(User).filter(User.login == login).first()
    if user is None:
        raise credentials_exception

    return user