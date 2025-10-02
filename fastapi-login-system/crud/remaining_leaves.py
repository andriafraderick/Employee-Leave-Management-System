from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import RemainingLeaves, LeaveDetails, LeaveTypes
from schemas import RemainingLeaveCreate, RemainingLeaveUpdate
from typing import Optional

async def get_leave_detail_id(db: AsyncSession, employee_id: str, leave_type: str) -> Optional[int]:
    """Helper function to find leave_detail_id"""
    result = await db.execute(
        select(LeaveDetails.id)
        .join(LeaveDetails.leave_type_obj)
        .where(
            LeaveDetails.employee_id == employee_id,
            LeaveTypes.leave_type == leave_type
        )
    )
    return result.scalar()

async def create_remaining_leave(db: AsyncSession, rem: RemainingLeaveCreate):
    try:
        # Find the matching leave_detail_id
        leave_detail_id = await get_leave_detail_id(db, rem.employee_id, rem.leave_type)
        if not leave_detail_id:
            raise ValueError(f"No leave details found for employee {rem.employee_id} and type {rem.leave_type}")

        # Create the new record
        db_rem = RemainingLeaves(
            leave_detail_id=leave_detail_id,
            total_leaves=rem.total_leaves,
            remaining_leaves=rem.remaining_leaves,
            year=rem.year
        )
        db.add(db_rem)
        await db.commit()
        await db.refresh(db_rem)
        return db_rem
    except Exception as e:
        await db.rollback()
        raise e

async def update_remaining_leave(
    db: AsyncSession, 
    leave_detail_id: int,
    rem: RemainingLeaveUpdate
):
    try:
        # Find existing record
        result = await db.execute(
            select(RemainingLeaves)
            .where(RemainingLeaves.leave_detail_id == leave_detail_id)
        )
        db_rem = result.scalars().first()
        
        if not db_rem:
            return None
            
        # Update only allowed fields
        if rem.remaining_leaves is not None:
            db_rem.remaining_leaves = rem.remaining_leaves
        if rem.total_leaves is not None:
            db_rem.total_leaves = rem.total_leaves
        
        await db.commit()
        await db.refresh(db_rem)
        return db_rem
    except Exception as e:
        await db.rollback()
        raise e