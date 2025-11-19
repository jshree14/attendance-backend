from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.db import base as db_base
from app.db import models
from app.schemas.student import StudentCreate, StudentOut
from app.core.config import UPLOAD_DIR
from app.utils.security import get_current_user, get_current_admin
import shutil, os

router = APIRouter(prefix="/students", tags=["students"])

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

@router.post("/", response_model=StudentOut, status_code=201)
def create_student(payload: StudentCreate, db: Session = Depends(db_base.get_db), current_user: int = Depends(get_current_admin)):
    existing = db.query(models.Student).filter(models.Student.roll_no == payload.roll_no).first()
    if existing:
        raise HTTPException(400, "Roll no already exists")
    s = models.Student(roll_no=payload.roll_no, name=payload.name, class_name=payload.class_name)
    db.add(s); db.commit(); db.refresh(s)
    return s

@router.get("/", response_model=list[StudentOut])
def list_students(class_name: str | None = None, db: Session = Depends(db_base.get_db), current_user: int = Depends(get_current_user)):
    q = db.query(models.Student)
    if class_name:
        q = q.filter(models.Student.class_name == class_name)
    return q.order_by(models.Student.name).all()

@router.get("/{student_id}", response_model=StudentOut)
def get_student(student_id: int, db: Session = Depends(db_base.get_db), current_user: int = Depends(get_current_user)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(404, "Student not found")
    return student

@router.post("/{student_id}/upload-photo", response_model=StudentOut)
def upload_photo(student_id: int, file: UploadFile = File(...), db: Session = Depends(db_base.get_db), current_user: int = Depends(get_current_user)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(404, "Student not found")
    
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"File type not allowed. Allowed: {', '.join(ALLOWED_EXTENSIONS)}")
    
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(400, f"File too large. Max size: {MAX_FILE_SIZE // (1024*1024)}MB")
    
    filename = f"{student_id}_{int(__import__('time').time())}{ext}"
    dest = UPLOAD_DIR / filename
    with open(dest, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    student.photo_path = str(dest)
    db.commit(); db.refresh(student)
    return student
