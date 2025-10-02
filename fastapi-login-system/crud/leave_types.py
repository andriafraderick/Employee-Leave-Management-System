from sqlalchemy.ext.asyncio import AsyncSession
from models import LeaveTypes
from schemas import LeaveTypeCreate

async def create_leave_type(db: AsyncSession, leave_type: LeaveTypeCreate):
    db_leave_type = LeaveTypes(**leave_type.dict())
    db.add(db_leave_type)
    await db.commit()
    await db.refresh(db_leave_type)
    return db_leave_type
