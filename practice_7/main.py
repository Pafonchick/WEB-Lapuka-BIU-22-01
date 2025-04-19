#Лапука Павел БИУ-22-01
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random

from database import SessionLocal, engine
from models import Base, User, Token
from schemas import UserLogin, TokenResponse, ChartInfo, ChartData
from auth import authenticate_user, create_access_token, get_current_user
from utils import generate_chart_data

app = FastAPI()

Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/login", response_model=TokenResponse)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_data.login, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.login})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/charts", response_model=list[ChartInfo])
async def get_charts_list(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return [
        {"id": 1, "name": "График температуры"},
        {"id": 2, "name": "График влажности"}
    ]

@app.get("/chart/{chart_id}", response_model=list[ChartData])
async def get_chart_data(
    chart_id: int,
    time_range: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    time_ranges = {
        "5m": (5/1440, 1),
        "1h": (1/24, 5),
        "1d": (1, 30),
        "2d": (2, 60)
    }

    if time_range not in time_ranges:
        raise HTTPException(
            status_code=400,
            detail="Invalid time_range. Allowed values: 5m, 1h, 1d, 2d"
        )

    duration_days, interval_minutes = time_ranges[time_range]

    if chart_id == 1:
        base_value = random.uniform(50, 60)
    elif chart_id == 2:
        base_value = random.uniform(30, 70)
    else:
        raise HTTPException(
            status_code=404,
            detail="Chart not found"
        )

    data = generate_chart_data(
        duration_days=duration_days,
        interval_minutes=interval_minutes,
        base_value=base_value
    )

    return data