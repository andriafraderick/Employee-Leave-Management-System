from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Profile
from schemas import ProfileCreate

async def get_profile_by_employee_id(db: AsyncSession, employee_id: str):
    result = await db.execute(select(Profile).where(Profile.employee_id == employee_id))
    return result.scalar_one_or_none()

async def create_or_update_profile(db: AsyncSession, employee_id: str, data: ProfileCreate):
    profile = await get_profile_by_employee_id(db, employee_id)
    if profile:
        for key, value in data.dict().items():
            setattr(profile, key, value)
    else:
        profile = Profile(**data.dict(), employee_id=employee_id)
        db.add(profile)

    await db.commit()
    await db.refresh(profile)
    return profile
