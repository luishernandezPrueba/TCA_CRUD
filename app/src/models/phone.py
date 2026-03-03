from sqlalchemy import Column, ForeignKey, Index, Integer, String, Enum, DateTime, func
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from models.base import Base

class PhoneType(PyEnum):
    MOBILE = 'mobile'
    HOME = 'home'
    WORK = 'work'


class Phone(Base):
    __tablename__ = 'phone'

    phone_id = Column(Integer, autoincrement=True, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.student_id'), primary_key=True)

    phone = Column(String(30), nullable=False)
    phone_type = Column(Enum(PhoneType), nullable=False)
    country_code = Column(String(5))
    area_code = Column(String(5))

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    student = relationship("Student", back_populates="phones")

    __table_args__ = (
        Index('student_phone_idx', 'student_id'),
    )