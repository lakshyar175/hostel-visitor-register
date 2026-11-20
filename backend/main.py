from fastapi import FastAPI, HTTPException,Header,Body
from fastapi.middleware.cors import CORSMiddleware
from datetime import date
import AM_functions as a
from typing import Optional
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/login")
def login(email=Body(),password=Body()):
    token=a.verify_login(email=email,password=password)
    if not token:
        raise HTTPException(status_code=401,detail="Access denied")
    return token

@app.post("/refresh")
def refresh_token(refresh_token=Header(None)):
    payload=a.verify_token(token=refresh_token,token_type="refresh")
    if not payload:
        raise HTTPException(status_code=401,detail="Invaild or token expired")
    access_token=a.create_token(email=payload["email"],token_type="access")
    return {"access_token":access_token}


@app.get("/visitors")
def get_visitor(access_token=Header(None)):
    payload=a.verify_token(token=access_token,token_type="access")
    if not payload:
        raise HTTPException(status_code=401,detail="Invalid or expired token")
    if payload["email"] != "email":
        raise HTTPException(status_code=403,detail="invalid credentials")
    return a.get_visitors_by_staff(email=payload["email"])