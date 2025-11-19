from pydantic import BaseModel, ConfigDict
from datetime import datetime
from datetime import date as date_type
from enum import Enum
from typing import Optional

class AttendanceStatus(str, Enum):
    present = "present"
    absent = "absent"
    leave = "leave"

class AttendanceMark(BaseModel):
    student_id: int
    status: AttendanceStatus
    date: Optional[date_type] = None
    note: Optional[str] = None

class AttendanceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    student_id: int
    attendance_date: date_type
    timestamp: datetime
    status: str
    note: Optional[str]
