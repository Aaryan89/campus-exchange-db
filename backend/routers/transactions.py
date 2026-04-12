from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import date
from database import get_connection

router = APIRouter()

class BorrowRequest(BaseModel):
    res_id: int
    sender_id: int
    receiver_id: int
    due_date: date

class WaitlistRequest(BaseModel):
    res_id: int
    stud_id: int