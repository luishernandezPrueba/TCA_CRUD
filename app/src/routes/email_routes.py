from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from services.email_service import create_email, delete_email, get_all_emails, get_emails_by_student_id, update_email
from database.database import get_db
from schemas.email import emailCreate, emailUpdate

router = APIRouter()

@router.post("/emails", response_model=emailCreate)
async def create_email_endpoint(email_data: emailCreate, db: AsyncSession = Depends(get_db)):
    return await create_email(email_data, db)

@router.get("/emails")
async def get_emails_endpoint(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await get_all_emails(db, skip, limit)

@router.get("/emails/student/{student_id}")
async def get_emails_by_student_id_endpoint(student_id: int, db: AsyncSession = Depends(get_db)):
    return await get_emails_by_student_id(student_id, db)

@router.patch("/emails/{email}")
async def patch_email_endpoint(email: str, email_data: emailUpdate, db: AsyncSession = Depends(get_db)):
    return await update_email(email, email_data, db)

@router.delete("/emails/{email}")
async def delete_email_endpoint(email: str, db: AsyncSession = Depends(get_db)):
    return await delete_email(email, db)