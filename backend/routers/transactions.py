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


@router.post("/borrow")
def borrow_resource(req: BorrowRequest):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc("sp_borrow_resource", [
            req.res_id, req.sender_id, req.receiver_id, str(req.due_date)
        ])
        for result in cursor.stored_results():
            return result.fetchone()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.post("/return/{tran_id}")
def return_resource(tran_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc("sp_return_resource", [tran_id])
        for result in cursor.stored_results():
            return result.fetchone()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.post("/waitlist")
def join_waitlist(req: WaitlistRequest):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc("sp_join_waitlist", [req.res_id, req.stud_id])
        for result in cursor.stored_results():
            return result.fetchone()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.get("/overdue")
def overdue_report():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc("sp_overdue_report")
        for result in cursor.stored_results():
            return result.fetchall()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.get("/student/{std_id}")
def student_transactions(std_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            """SELECT t.*, r.title AS resource_title,
                      sender.name   AS sender_name,
                      receiver.name AS receiver_name
               FROM Transactions t
               JOIN Resources r  ON r.res_id  = t.res_id
               JOIN Students sender   ON sender.std_id   = t.sender_id
               JOIN Students receiver ON receiver.std_id = t.receiver_id
               WHERE t.sender_id = %s OR t.receiver_id = %s
               ORDER BY t.issue_date DESC""",
            (std_id, std_id)
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


@router.get("/active-borrows/{std_id}")
def active_borrows(std_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT fn_active_borrows(%s)", (std_id,))
        row = cursor.fetchone()
        return {"std_id": std_id, "active_borrows": row[0]}
    finally:
        cursor.close()
        conn.close()