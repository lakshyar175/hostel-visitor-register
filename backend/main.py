from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from datetime import date
import SU_functions as s
import AM_functions as a

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Staff(BaseModel):
    username: str = Field(min_length=1)
    email: EmailStr
    password: str = Field(min_length=1)

class Visitor(BaseModel):
    visitor_name: str = Field(min_length=1)
    student_name: str = Field(min_length=1)
    room_no: str = Field(min_length=1)
    purpose: str = Field(min_length=1)
    visit_date: date


#A1
@app.post("/register")
def register_staff(username: Staff):
    result = s.register_staff(username=username.username,email=username.email,password=username.password)
    if result is None:
        raise HTTPException(status_code=409, detail="Email already exists")
    return result


#E2

@app.post("/visitors")
def register_visitor(visitor: Visitor, access_token=Header(None)):
    payload = a.verify_token(token=access_token, token_type="access")
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    result = s.register_visitor(
        username=payload["username"],
        visitor_name=visitor.visitor_name,
        student_name=visitor.student_name,
        room_no=visitor.room_no,
        purpose=visitor.purpose,
        visit_date=visitor.visit_date
    )
    if result is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return result