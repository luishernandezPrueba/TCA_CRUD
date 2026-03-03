from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Address,Student
from schemas.address import addressCreate, addressUpdate



async def create_address(address_data: addressCreate, db: AsyncSession):
    try:
        db_address = Address(**address_data.model_dump(exclude_unset=True))

        validate_student = await db.execute(select(Student).where(Student.student_id == db_address.student_id))
        if validate_student.scalar_one_or_none() is None:
            raise HTTPException(status_code=404, detail=f"Student with id {db_address.student_id} not found")

        db.add(db_address)
        await db.commit()
        await db.refresh(db_address)
        return db_address
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, detail=str(e))

async def get_all_addresses(db:AsyncSession, skip: int = 0, limit: int = 100):
    try:
        results = await db.execute(select(Address).offset(skip).limit(limit))
        addresses = results.scalars().all()
        return addresses
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, detail=str(e))
    
async def get_address_by_id(address_id: int, db: AsyncSession):
    try:
        result = await db.execute(select(Address).where(Address.address_id == address_id))
        address = result.scalar_one_or_none()
        if address is None:
            raise HTTPException(status_code=404, detail="Address not found")
        return address
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, detail=str(e))
    
async def get_addresses_by_student_id(student_id: int, db: AsyncSession):
    try:
        result = await db.execute(select(Address).where(Address.student_id == student_id))
        addresses = result.scalars().all()
        return addresses
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, detail=str(e))

async def get_addresses_by_city(city: str, db: AsyncSession):
    try:
        result = await db.execute(select(Address).where(Address.city == city))
        addresses = result.scalars().all()
        if not addresses:
            raise HTTPException(status_code=404, detail=f"No addresses found in city {city}")
        return addresses
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, detail=str(e))
    

async def update_address(address_id: int, address_data: addressUpdate, db: AsyncSession):
    try:
        result = await db.execute(select(Address).where(Address.address_id == address_id))
        address = result.scalar_one_or_none()
        if address is None:
            raise HTTPException(status_code=404, detail="Address not found")
        
        for key, value in address_data.model_dump().items():
            setattr(address, key, value)
        await db.commit()
        await db.refresh(address)
        return { "message" : "Address updated succesfully!"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, detail=str(e))
    
async def delete_address(address_id: int, db: AsyncSession):
    try:
        result = await db.execute(select(Address).where(Address.address_id == address_id))
        address = result.scalar_one_or_none()
        if address is None:
            raise HTTPException(status_code=404, detail="Address not found")
        await db.delete(address)
        await db.commit()
        return { "message" : "Address deleted succesfully!"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, detail=str(e))