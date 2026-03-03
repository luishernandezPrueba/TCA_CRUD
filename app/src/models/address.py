from sqlalchemy import Column, ForeignKey, Index, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from models.base import Base

class Address(Base):
    __tablename__ = 'address'
    
    address_id = Column(Integer, autoincrement=True, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.student_id'), primary_key=True)
    
    address_line = Column(String(100))
    city = Column(String(45))
    zip_postcode = Column(String(45))
    state = Column(String(45))
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    student = relationship("Student", back_populates="addresses")
    
    __table_args__ = (
        Index('address_student_idx', 'student_id'),
    )
