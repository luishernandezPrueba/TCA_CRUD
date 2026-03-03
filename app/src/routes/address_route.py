from fastapi import APIRouter, Depends, HTTPException
from database.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from services.address_service import *
from schemas.address import addressCreate, addressUpdate

router = APIRouter()

@router.post("/addresses", response_model=addressCreate)
async def create_address_endpoint(address_data: addressCreate, db: AsyncSession = Depends(get_db)):
    return await create_address(address_data, db)

@router.get("/addresses")
async def get_addresses_endpoint(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await get_all_addresses(db, skip, limit)

@router.get("/addresses/{address_id}")
async def get_address_endpoint(address_id: int, db: AsyncSession = Depends(get_db)):
    return await get_address_by_id(address_id, db)

@router.get("/addresses/student/{student_id}")
async def get_addresses_by_student_id_endpoint(student_id: int, db: AsyncSession = Depends(get_db)):
    return await get_addresses_by_student_id(student_id, db)

@router.get("/addresses/city/{city}")
async def get_addresses_by_city_endpoint(city: str, db: AsyncSession = Depends(get_db)):
    return await get_addresses_by_city(city, db)

@router.patch("/addresses/{address_id}")
async def patch_address_endpoint(address_id: int, address_data: addressUpdate, db: AsyncSession = Depends(get_db)):
    return await update_address(address_id, address_data, db)

@router.delete("/addresses/{address_id}")
async def delete_address_endpoint(address_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_address(address_id, db)
