from fastapi import APIRouter, HTTPException
from database import get_connection
from typing import Optional
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext

router = APIRouter()

class DonateRequest(BaseModel):
    title: str
    author_model: Optional[str] = None
    category: Optional[str] = None
    donor_id: int
    condition: str