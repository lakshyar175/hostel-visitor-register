from sqlalchemy import Integer, String, Column, ForeignKey, create_engine,Date,func,Float, DateTime
from sqlalchemy.orm import Session, declarative_base
from fastapi import FastAPI, HTTPException
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from pydantic import BaseModel,Field
from typing import Optional
from datetime import date,datetime,timedelta,timezone

ph = PasswordHasher()

#A1
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
    session.refresh(new_user)
    response = {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "created_at": new_user.created_at
    }
    session.close()
    return response


#E2
def register_visitor(username, visitor_name, student_name, room_no, purpose, visit_date):
    session = Session(engine)
    user = session.query(User).filter_by(username=username).first()
    if not user:
        session.close()
        return None
    new_visitor = Visitor(user_id=user.id,visitor_name=visitor_name,student_name=student_name,room_no=room_no,purpose=purpose,visit_date=visit_date)
    session.add(new_visitor)
    session.commit()
    session.refresh(new_visitor)
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

