from pydantic import BaseModel, Field, EmailStr
from enum import Enum
from typing import Optional

class emailTypeEnum(str, Enum):
    PERSONAL = 'personal'
    WORK = 'work'
    SCHOOL = 'school'

class emailBase(BaseModel):
    student_id: int
    email: EmailStr = Field(..., max_length=100)
    email_type: emailTypeEnum

class emailCreate(emailBase):
    pass

class emailUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, max_length=100)
    email_type: Optional[emailTypeEnum] = None
