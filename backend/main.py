from fastapi import FastAPI, HTTPException,Header,Body
from fastapi.middleware.cors import CORSMiddleware
from datetime import date

from typing import Optional
app = FastAPI()
from pydantic import BaseModel, EmailStr, Field
from datetime import date
import functions as f


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

class LoginIn(BaseModel):
    email: EmailStr          
    password: str = Field(min_length=1)

class VisitorIn(BaseModel):
    visitor_name: str = Field(min_length=1)
    student_name: str = Field(min_length=1)
    room_no: str = Field(min_length=1)
    purpose: str = Field(min_length=1)
    visit_date: date
    
#A1
@app.post("/regis")
def register_staff(username: Staff):
    result = f.register_staff(username=username.username,email=username.email,password=username.password)
    if result is None:
        raise HTTPException(status_code=409, detail="Email already exists")
    return result

@app.post("/login")
def login(l: LoginIn):
    token = f.verify_login(email=l.email, password=l.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return token

@app.post("/refresh")
def refresh_token(refresh_token=Header(None)):
    payload=f.verify_token(token=refresh_token,token_type="refresh")
    if not payload:
        raise HTTPException(status_code=401,detail="Invaild or token expired")
    access_token=f.create_token(email=payload["email"],token_type="access")
    return {"access_token":access_token}

@app.get("/visitors")
def get_visitor(access_token=Header(None)):
    payload=f.verify_token(token=access_token,token_type="access")
    if not payload:
        raise HTTPException(status_code=401,detail="Invalid or expired token")
    
    return f.get_visitors_by_staff(email=payload["email"])

#E2

@app.post("/visitors")
def register_visitor(visitor: VisitorIn, access_token=Header(None)):
    payload = f.verify_token(token=access_token, token_type="access")
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    result = f.register_visitor(
        email=payload["email"],
        visitor_name=visitor.visitor_name,
        student_name=visitor.student_name,
        room_no=visitor.room_no,
        purpose=visitor.purpose,
        visit_date=visitor.visit_date
    )
    if result is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return result


