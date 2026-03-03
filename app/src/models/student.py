from sqlalchemy import Column, Index, Integer, String, Enum, DateTime, func
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from models.base import Base

class Gender(PyEnum):
    M = 'M'
    F = 'F'
    O = 'O'

class Student(Base):
    __tablename__ = 'students'
    
    student_id = Column(Integer, primary_key=True, index=True)
    last_name = Column(String(45), nullable=False)
    middle_name = Column(String(45))
    first_name = Column(String(45))
    gender = Column(Enum(Gender), nullable=False)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    addresses = relationship("Address", back_populates="student", cascade="all, delete-orphan")
    emails = relationship("Email", back_populates="student", cascade="all, delete-orphan")
    phones = relationship("Phone", back_populates="student", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('student_last_name_idx', 'last_name'),
    )
