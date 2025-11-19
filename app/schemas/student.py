from pydantic import BaseModel, ConfigDict
from typing import Optional

class StudentCreate(BaseModel):
    roll_no: str
    name: str
    class_name: Optional[str] = None

class StudentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    roll_no: str
    name: str
    class_name: Optional[str]
    photo_path: Optional[str]
