from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from services.phone_service import create_phone, delete_phone, get_all_phones, get_phone_by_id, get_phones_by_student_id, update_phone
from database.database import get_db
from schemas.phone import phoneCreate, phoneUpdate

router = APIRouter()

@router.post("/phones", response_model=phoneCreate)
async def create_phone_endpoint(phone_data: phoneCreate, db: AsyncSession = Depends(get_db)):
    return await create_phone(phone_data, db)   

@router.get("/phones")
async def get_phones_endpoint(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await get_all_phones(db, skip, limit)

@router.get("/phones/{phone_id}")
async def get_phone_endpoint(phone_id: int, db: AsyncSession = Depends(get_db)):
    return await get_phone_by_id(phone_id, db)  

@router.get("/phones/student/{student_id}")
async def get_phones_by_student_id_endpoint(student_id: int, db: AsyncSession = Depends(get_db)):
    return await get_phones_by_student_id(student_id, db)   

@router.patch("/phones/{phone_id}")
async def patch_phone_endpoint(phone_id: int, phone_data: phoneUpdate, db: AsyncSession = Depends(get_db)):
    return await update_phone(phone_id, phone_data, db)

@router.delete("/phones/{phone_id}")
async def delete_phone_endpoint(phone_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_phone(phone_id, db) 