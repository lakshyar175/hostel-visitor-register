from sqlalchemy import Integer, String, Column, ForeignKey, create_engine,Date,func,Float, DateTime
from sqlalchemy.orm import Session, declarative_base
from fastapi import FastAPI, HTTPException
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from pydantic import BaseModel,Field
from typing import Optional
from datetime import date,datetime,timedelta,timezone

ph=PasswordHasher()

ACCEESS_TOKEN_EXPIRY=60
REFRESH_TOKEN_EXPIRY=7*24*60
SECRET_KEY="SECRETway"
ALGORITHM="HS256"

DB_PATH = "visitors.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id=Column(Integer,primary_key=True)
    username=Column(String)
    email=Column(String)
    hashed_password=Column(String)
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

class UserIn(BaseModel):
    username:str
    user_type:str
    hashed_password:str
    email:str
    created_at:date

def create_token(email,token_type):
    time = ACCEESS_TOKEN_EXPIRY
    if token_type == "refresh":
        time = REFRESH_TOKEN_EXPIRY
    payload={
        "email":email,
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

def verify_login(email,password):
    session=Session(engine)
    user=session.query(User).filter_by(email=email.lower()).first()
    if user is None:
        session.close()
        return False
    try:
        ph.verify(user.hashed_password,password)
    except VerifyMismatchError:
        session.close()
        return False    
    tokens={
        "access_token":create_token(email=email,token_type="access"),
        "refresh_token":create_token(email=email,token_type="refresh")
    }
    session.close()
    return tokens


def register_staff(username, email, password):
    session = Session(engine)
    email = email.strip().lower()
    user = session.query(User).filter_by(email=email).first()
    if user:
        session.close()
        return None
    new_user = User(username=username,email=email,hashed_password=ph.hash(password))
    session.add(new_user)
    session.commit()
    response = {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "created_at": new_user.created_at
    }
    session.close()
    return response


def register_visitor(email,visitor_name, student_name, room_no, purpose, visit_date):
    session = Session(engine)
    email = email.strip().lower()
    user = session.query(User).filter_by(email=email).first()
    if not user:
        session.close()
        return None
    new_visitor = Visitor(user_id=user.id,visitor_name=visitor_name,student_name=student_name,room_no=room_no,purpose=purpose,visit_date=visit_date)
    session.add(new_visitor)
    session.commit()
    response = {
        "id": new_visitor.id,
        "visitor_name": new_visitor.visitor_name,
        "student_name": new_visitor.student_name,
        "room_no": new_visitor.room_no,
        "purpose": new_visitor.purpose,
        "visit_date": new_visitor.visit_date,
        "created_at": new_visitor.created_at
    }
    session.close()
    return response


def get_visitors_by_staff(email):
    session=Session(engine)
    email = email.strip().lower()
    user=session.query(User).filter_by(email=email.lower()).first()
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
