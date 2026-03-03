from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class GenderEnum(str, Enum):
    M = 'M'
    F = 'F'
    O = 'O'

class studentBase(BaseModel):
    last_name: str = Field(..., min_length=1, max_length=45)
    middle_name: Optional[str] = Field(None, max_length=45)
    first_name: Optional[str] = Field(None, max_length=45)
    gender: GenderEnum

class studentCreate(studentBase):
    pass

class studentUpdate(studentBase):
    last_name: Optional[str] = Field(None, min_length=1, max_length=45)
    gender: Optional[GenderEnum] = None