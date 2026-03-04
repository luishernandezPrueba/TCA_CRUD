from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Phone, Student
from schemas.phone import phoneCreate, phoneUpdate

async def create_phone(phone_data: phoneCreate, db: AsyncSession):
    try:
        db_phone = Phone(**phone_data.model_dump(exclude_unset=True))

        validate_student = await db.execute(select(Student).where(Student.student_id == db_phone.student_id))
        if validate_student.scalar_one_or_none() is None:
            raise HTTPException(status_code=404, detail=f"Student with id {db_phone.student_id} not found")
        
        validate_duplicate_phone = await db.execute(select(Phone).where(Phone.phone == db_phone.phone))
        if validate_duplicate_phone.scalar_one_or_none() is not None:
            raise HTTPException(status_code=400, detail=f"Phone {db_phone.phone} already exists")

        db.add(db_phone)
        await db.commit()
        await db.refresh(db_phone)
        return db_phone
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, detail=str(e))
    
async def get_all_phones(db: AsyncSession, skip: int = 0, limit: int = 100):
    try:
        results = await db.execute(select(Phone).offset(skip).limit(limit))
        phones = results.scalars().all()
        return phones
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, detail=str(e))
    
async def get_phone_by_id(phone_id: int, db: AsyncSession):
    try:
        result = await db.execute(select(Phone).where(Phone.phone_id == phone_id))
        phone = result.scalar_one_or_none()
        if phone is None:
            raise HTTPException(status_code=404, detail="Phone not found")
        return phone
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, detail=str(e))
    
async def get_phones_by_student_id(student_id: int, db: AsyncSession):
    try:
        result = await db.execute(select(Phone).where(Phone.student_id == student_id))
        phones = result.scalars().all()
        return phones
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, detail=str(e))
    
async def update_phone(phone_id: int, phone_data: phoneUpdate, db: AsyncSession):
    try:
        result = await db.execute(select(Phone).where(Phone.phone_id == phone_id))
        phone = result.scalar_one_or_none()
        if phone is None:
            raise HTTPException(status_code=404, detail="Phone not found")
        
        if phone_data.phone and phone_data.phone != phone.phone:
            duplicate = await db.execute(select(Phone).where(Phone.phone == phone_data.phone))
            if duplicate.scalar_one_or_none() is not None:
                raise HTTPException(status_code=400, detail=f"Phone {phone_data.phone} already exists")
        
        for key, value in phone_data.model_dump(exclude_unset=True).items():
            setattr(phone, key, value)

        await db.commit()
        await db.refresh(phone)
        return phone
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, detail=str(e))
    
async def delete_phone(phone_id: int, db: AsyncSession):
    try:
        result = await db.execute(select(Phone).where(Phone.phone_id == phone_id))
        phone = result.scalar_one_or_none()
        if phone is None:
            raise HTTPException(status_code=404, detail="Phone not found")
        
        await db.delete(phone)
        await db.commit()
        return {"detail": "Phone deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, detail=str(e))