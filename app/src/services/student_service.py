from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Student
from schemas.student import studentCreate, studentUpdate


async def create_student(student_data: studentCreate, db: AsyncSession):
    try:
        db_student = Student(**student_data.model_dump())
        db.add(db_student)
        await db.commit()
        await db.refresh(db_student)
        return db_student
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def get_all_students(db: AsyncSession):
    try:
        result = await db.execute(select(Student))
        students = result.scalars().all()
        return students
    except HTTPException as e:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def get_student_by_id(student_id: int, db: AsyncSession):
    try:
        result = await db.execute(select(Student).where(Student.student_id == student_id))
        student = result.scalar_one_or_none()
        if student is None:
            raise HTTPException(status_code=404, detail="Student not found")
        return student
    except HTTPException as e:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def get_student_by_last_name(student_last_name: str, db: AsyncSession):
    try:
        result = await db.execute(select(Student).where(Student.last_name == student_last_name))
        students = result.scalars().all()
        if not students:
            raise HTTPException(status_code=404, detail=f"No students found with last name {student_last_name}")
        return students
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

async def update_student(student_id: int, student_data: studentUpdate, db: AsyncSession):
    try:
        result = await db.execute(select(Student).where(Student.student_id == student_id))
        student = result.scalar_one_or_none()
        if student is None:
            raise HTTPException(status_code=404, detail="Student not found")
        
        for key, value in student_data.model_dump(exclude_unset=True).items():
            setattr(student, key, value)
        
        await db.commit()
        await db.refresh(student)
        return student
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def delete_student(student_id: int, db: AsyncSession):
    try:
        result = await db.execute(select(Student).where(Student.student_id == student_id))
        student = result.scalar_one_or_none()
        if student is None:
            raise HTTPException(status_code=404, detail="Student not found")
        
        await db.delete(student)
        await db.commit()
        return {"detail": "Student deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))