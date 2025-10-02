from sqlalchemy.ext.asyncio import AsyncSession
from models import LeaveDetails
from schemas import LeaveDetailCreate

async def create_leave_detail(db: AsyncSession, detail: LeaveDetailCreate):
    db_detail = LeaveDetails(**detail.dict())
    db.add(db_detail)
    await db.commit()
    await db.refresh(db_detail)
    return db_detail
