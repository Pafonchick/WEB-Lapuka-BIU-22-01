from pydantic import BaseModel
from typing import List

class UserLogin(BaseModel):
    login: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class ChartInfo(BaseModel):
    id: int
    name: str

class ChartData(BaseModel):
    timestamp: str
    value: float