from pydantic import BaseModel, Field
from typing import Optional

class addressBase(BaseModel):
    student_id: int
    address_line: Optional[str] = Field(None, max_length=100)
    city: Optional[str] = Field(None, max_length=45)
    zip_postcode: Optional[str] = Field(None, max_length=45)
    state: Optional[str] = Field(None, max_length=45)

class addressCreate(addressBase):
    pass

class addressUpdate(BaseModel):
    address_line: Optional[str] = Field(None, max_length=100)
    city: Optional[str] = Field(None, max_length=45)
    zip_postcode: Optional[str] = Field(None, max_length=45)
    state: Optional[str] = Field(None, max_length=45)