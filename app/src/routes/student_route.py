from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from services.student_service import create_student, delete_student, get_all_students, get_student_by_id, get_student_by_last_name, update_student
from database.database import get_db
from schemas.student import studentCreate, studentUpdate

router = APIRouter()

@router.post("/students", response_model=studentCreate)
async def create_student_endpoint(student_data: studentCreate, db: AsyncSession = Depends(get_db)):
    return await create_student(student_data, db)

@router.get("/students")
async def get_students_endpoint(db: AsyncSession = Depends(get_db)):
    return await get_all_students(db)

@router.get("/students/{student_id}")
async def get_student_endpoint(student_id: int, db: AsyncSession = Depends(get_db)):
    return await get_student_by_id(student_id, db)

@router.get("/students/lastName/{student_last_name}")
async def get_student_by_lastname(student_last_name:str, db: AsyncSession = Depends(get_db)):
    return await get_student_by_last_name(student_last_name, db)

@router.patch("/students/{student_id}")
async def update_student_endpoint(student_id: int, student_data: studentUpdate , db: AsyncSession = Depends(get_db)):
    return await update_student(student_id, student_data, db)

@router.delete("/students/{student_id}")
async def delete_student_endpoint(student_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_student(student_id, db)