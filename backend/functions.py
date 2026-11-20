from sqlalchemy import Integer, String, Column, create_engine, DateTime, Date, ForeignKey
from sqlalchemy.orm import declarative_base
from datetime import datetime

DB_PATH = "visitors.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

# LA_FUNCTIONS
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.now)

class Visitor(Base):
    __tablename__ = "visitors"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    visitor_name = Column(String)
    student_name = Column(String)
    room_no = Column(String)
    purpose = Column(String)
    visit_date = Column(Date)
    created_at = Column(DateTime, default=datetime.now)

Base.metadata.create_all(engine)

