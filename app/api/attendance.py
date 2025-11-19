from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import exc
from app.db import base as db_base
from app.db import models
from app.schemas.attendance import AttendanceMark, AttendanceOut
from app.utils.security import get_current_user
from datetime import datetime, date, UTC
import csv
import io

router = APIRouter(prefix="/attendance", tags=["attendance"])

@router.post("/mark", response_model=AttendanceOut)
def mark_attendance(payload: AttendanceMark, db: Session = Depends(db_base.get_db), current_user: int = Depends(get_current_user)):
    student = db.query(models.Student).filter(models.Student.id == payload.student_id).first()
    if not student:
        raise HTTPException(404, "Student not found")
    
    att_date = payload.date if payload.date else date.today()
    
    try:
        att = models.Attendance(
            student_id=payload.student_id, 
            status=payload.status, 
            note=payload.note, 
            marked_by=current_user,
            attendance_date=att_date,
            timestamp=datetime.now(UTC)
        )
        db.add(att)
        db.commit()
        db.refresh(att)
        return att
    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(400, "Attendance already marked for this student on this date")

@router.get("/", response_model=list[AttendanceOut])
def list_attendance(
    student_id: int | None = None, 
    class_name: str | None = None, 
    from_date: date | None = None, 
    to_date: date | None = None, 
    db: Session = Depends(db_base.get_db),
    current_user: int = Depends(get_current_user)
):
    q = db.query(models.Attendance).join(models.Student)
    
    if student_id:
        q = q.filter(models.Attendance.student_id == student_id)
    if class_name:
        q = q.filter(models.Student.class_name == class_name)
    if from_date:
        q = q.filter(models.Attendance.attendance_date >= from_date)
    if to_date:
        q = q.filter(models.Attendance.attendance_date <= to_date)
    
    return q.order_by(models.Attendance.attendance_date.desc()).all()

@router.get("/export")
def export_attendance_csv(
    student_id: int | None = None,
    class_name: str | None = None,
    from_date: date | None = None,
    to_date: date | None = None,
    db: Session = Depends(db_base.get_db),
    current_user: int = Depends(get_current_user)
):
    q = db.query(models.Attendance, models.Student).join(models.Student)
    
    if student_id:
        q = q.filter(models.Attendance.student_id == student_id)
    if class_name:
        q = q.filter(models.Student.class_name == class_name)
    if from_date:
        q = q.filter(models.Attendance.attendance_date >= from_date)
    if to_date:
        q = q.filter(models.Attendance.attendance_date <= to_date)
    
    records = q.order_by(models.Attendance.attendance_date.desc()).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Roll No", "Student Name", "Class", "Date", "Status", "Note", "Marked At"])
    
    for att, student in records:
        writer.writerow([
            att.id,
            student.roll_no,
            student.name,
            student.class_name or "",
            att.attendance_date.strftime("%Y-%m-%d"),
            att.status,
            att.note or "",
            att.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        ])
    
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=attendance_export.csv"}
    )
