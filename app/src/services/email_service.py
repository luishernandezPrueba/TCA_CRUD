from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Email, Student
from schemas.email import emailCreate, emailUpdate

async def create_email(email_data: emailCreate, db: AsyncSession):
    try:
        db_email = Email(**email_data.model_dump(exclude_unset=True))

        validate_student = await db.execute(select(Student).where(Student.student_id == db_email.student_id))
        if validate_student.scalar_one_or_none() is None:
            raise HTTPException(status_code=404, detail=f"Student with id {db_email.student_id} not found")
        
        validate_duplicate_email = await db.execute(select(Email).where(Email.email == db_email.email))
        if validate_duplicate_email.scalar_one_or_none() is not None:
            raise HTTPException(status_code=400, detail=f"Email {db_email.email} already exists")

        db.add(db_email)
        await db.commit()
        await db.refresh(db_email)
        return db_email
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, detail=str(e))
    
async def get_all_emails(db:AsyncSession, skip: int = 0, limit: int = 100):
    try:
        results = await db.execute(select(Email).offset(skip).limit(limit))
        emails = results.scalars().all()
        return emails
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, detail=str(e))
    
    
async def get_emails_by_student_id(student_id: int, db: AsyncSession):
    try:
        result = await db.execute(select(Email).where(Email.student_id == student_id))
        emails = result.scalars().all()
        # return empty list if none found instead of 404
        return emails
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, detail=str(e))
    
async def update_email(email: str, email_data: emailUpdate, db: AsyncSession):
    try:
        result = await db.execute(select(Email).where(Email.email == email))
        email = result.scalar_one_or_none()
        if email is None:
            raise HTTPException(status_code=404, detail="Email not found")
        
        for key, value in email_data.model_dump(exclude_unset=True).items():
            setattr(email, key, value)

        await db.commit()
        await db.refresh(email)
        return email
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, detail=str(e))
    
async def delete_email(email: str, db: AsyncSession):
    try:
        result = await db.execute(select(Email).where(Email.email == email))
        email = result.scalar_one_or_none()
        if email is None:
            raise HTTPException(status_code=404, detail="Email not found")
        
        await db.delete(email)
        await db.commit()
        return {"detail": "Email deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, detail=str(e))