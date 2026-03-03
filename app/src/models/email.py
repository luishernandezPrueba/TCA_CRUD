from sqlalchemy import Column, ForeignKey, Index, Integer, String, Enum, DateTime, func
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from models.base import Base


class EmailType(PyEnum):
    PERSONAL = 'personal'
    WORK = 'work'
    SCHOOL = 'school'

class Email(Base):
    __tablename__ = 'email'

    email = Column(String(100), primary_key=True)
    student_id = Column(Integer, ForeignKey('students.student_id'), primary_key=True)

    email_type = Column(Enum(EmailType), nullable=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    student = relationship("Student", back_populates="emails")

    __table_args__ = (
        Index('student_email_fk_idx', 'student_id'),
    )