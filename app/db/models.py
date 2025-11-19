from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Date, UniqueConstraint
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime, UTC

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    roll_no = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    class_name = Column(String, index=True)
    photo_path = Column(String, nullable=True)

class Attendance(Base):
    __tablename__ = "attendance"
    __table_args__ = (UniqueConstraint('student_id', 'attendance_date', name='_student_date_uc'),)
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    attendance_date = Column(Date, index=True, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(UTC))
    status = Column(String)  # "present", "absent", "leave"
    marked_by = Column(Integer, ForeignKey("users.id"))
    note = Column(String, nullable=True)

    student = relationship("Student", backref="attendance_records")
