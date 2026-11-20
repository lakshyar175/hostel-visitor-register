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

# @app.post("/register")
# def register(u:a.UserIn):
#     if a.register_user(username=u.username,user_type=u.user_type.lower(),password=u.password,email=u.email,created_at=u.created_at):
#         return{"message":"user registered successfully"}
#     raise HTTPException(status_code=400,detail="User email already exists")

@app.post("/login")
def login(username=Body(),password=Body()):
    token=a.verify_login(username=username,password=password)
    if not token:
        raise HTTPException(status_code=401,detail="Access denied")
    return token

@app.post("/refresh")
def refresh_token(refresh_token=Header(None)):
    payload=a.verify_token(token=refresh_token,token_type="refresh")
    if not payload:
        raise HTTPException(status_code=401,detail="Invaild or token expired")
    access_token=a.create_token(username=payload["username"],user_type=payload["user_type"],token_type="access")
    return {"access_token":access_token}


@app.get("/visitors")
def get_visitor(access_token=Header(None)):
    payload=a.verify_token(token=access_token,token_type="access")
    if not payload:
        raise HTTPException(status_code=401,detail="Invalid or expired token")
    if payload["user_type"] != "staff":
        raise HTTPException(status_code=403,detail="Only staff can view this")
    return a.get_visitors_by_staff(username=payload["username"])