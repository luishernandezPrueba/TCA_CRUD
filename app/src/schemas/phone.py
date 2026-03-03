from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class phoneTypeEnum(str, Enum):
    MOBILE = 'mobile'
    HOME = 'home'
    WORK = 'work'

class phoneBase(BaseModel):
    student_id: int
    phone: str = Field(..., max_length=30)
    phone_type: phoneTypeEnum
    country_code: Optional[str] = Field(None, max_length=5)
    area_code: Optional[str] = Field(None, max_length=5)

class phoneCreate(phoneBase):
    pass

class phoneUpdate(BaseModel):
    phone: Optional[str] = Field(None, max_length=30)
    phone_type: Optional[phoneTypeEnum] = None
    country_code: Optional[str] = Field(None, max_length=5)
    area_code: Optional[str] = Field(None, max_length=5)


