from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import get_db
from auth.auth import get_current_user
from schemas import ProfileResponse, ProfileCreate
from crud.profile import get_profile_by_employee_id, create_or_update_profile

router = APIRouter()

@router.get("/profile/{employee_id}", response_model=ProfileResponse)
async def read_profile_by_employee_id(
    employee_id: str,
    db: AsyncSession = Depends(get_db)
):
    profile = await get_profile_by_employee_id(db, employee_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.post("/profile/update/{employee_id}", response_model=ProfileResponse)
async def update_profile_by_employee_id(
    employee_id: str,
    data: ProfileCreate,
    db: AsyncSession = Depends(get_db)
):
    return await create_or_update_profile(db, employee_id, data)

