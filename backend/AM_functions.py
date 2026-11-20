from sqlalchemy import Integer, String, Column, ForeignKey, create_engine,Date,func,Float
from sqlalchemy.orm import Session, declarative_base
from fastapi import FastAPI, HTTPException
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from pydantic import BaseModel,Field
from typing import Optional

from datetime import date,datetime,timedelta,timezone

ph=PasswordHasher()

DB_PATH = "visitors.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()


class UserIn(BaseModel):
    username:str
    user_type:str
    hashed_password:str
    email:str
    created_at:date

ACCEESS_TOKEN_EXPIRY=60
REFRESH_TOKEN_EXPIRY=7*24*60
SECRET_KEY="SECRETway"
ALGORITHM="HS256"

class User(Base):
    __tablename__ = "users"

    id=Column(Integer,primary_key=True)
    username=Column(String)
    user_type=Column(String)
    hashed_password=Column(String)
    email=Column(String) 
    created_at=Column(Date,default=date.today)

class Visitor(Base):
    __tablename__ = "visitors"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    visitor_name = Column(String)
    student_name = Column(String)
    room_no = Column(String)
    purpose = Column(String)
    visit_date = Column(Date)
    created_at = Column(Date, default=date.today)

Base.metadata.create_all(engine)    

# def register_user(username,user_type,hashed_password,email,created_at):
#     if user_type not in ["visitor","staff"]:
#         raise HTTPException(status_code=422,detail="Invalid user type")
#     session=Session(engine)
#     user=session.query(User).filter_by(email=email).first()
#     if user is not None:
#         session.close()
#         return False
#     session.add(User(username=username,hashed_password=ph.hash(hashed_password),user_type=user_type.lower(),email=email,created_at=created_at))
#     session.commit()
#     session.close()
#     return True

def create_token(username,user_type,token_type):
    time = ACCEESS_TOKEN_EXPIRY
    if token_type == "refresh":
        time = REFRESH_TOKEN_EXPIRY
    payload={
        "username":username,
        "user_type":user_type,
        "token_type":token_type,
        "exp":datetime.now(timezone.utc)+timedelta(minutes=time)
    }    
    token=jwt.encode(payload=payload,key=SECRET_KEY,algorithm=ALGORITHM)
    return token

def verify_token(token,token_type):
    try:
        payload=jwt.decode(token,key=SECRET_KEY,algorithms=[ALGORITHM])
    except:
        return False

    if payload["token_type"] != token_type:
        return False
    return payload

def verify_login(username,hashed_password):
    session=Session(engine)
    user=session.query(User).filter_by(username=username).first()
    if user is None:
        session.close()
        return False
    try:
        ph.verify(user.hashed_password,hashed_hashed_password)
    except VerifyMismatchError:
        session.close()
        return False    
    tokens={
        "access_token":create_token(username=username,user_type=user.user_type,token_type="access"),
        "refresh_token":create_token(username=username,user_type=user.user_type,token_type="refresh")
    }
    session.close()
    return tokens

def get_visitors_by_staff(username):
    session=Session(engine)
    user=session.query(User).filter_by(username=username).first()
    if user is None:
        session.close()
        return []
    visitors=session.query(Visitor).filter_by(user_id=user.id).all()
    result=[]
    for v in visitors:
        result.append({
            "id":v.id,
            "visitor_name":v.visitor_name,
            "student_name":v.student_name,
            "room_no":v.room_no,
            "purpose":v.purpose,
            "visit_date":v.visit_date,
            "created_at":v.created_at
        })
    session.close()
    return result