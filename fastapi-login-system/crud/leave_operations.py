from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import RemainingLeaves, LeaveDetails, LeaveTypes
from datetime import datetime

async def apply_leave_and_update_balance(
    db: AsyncSession,
    employee_id: str,
    days_applied: int,
    leave_type: str = "casual",
    clear_lop: bool = True
):
    try:
        # 1. Get the leave detail record for this employee and leave type
        leave_detail = await db.execute(
            select(LeaveDetails)
            .join(LeaveDetails.leave_type_obj)
            .where(
                LeaveDetails.employee_id == employee_id,
                LeaveTypes.leave_type == leave_type
            )
        )
        leave_detail = leave_detail.scalars().first()
        
        if not leave_detail:
            raise ValueError(f"No leave details found for employee {employee_id} and leave type {leave_type}")

        # 2. Get the current remaining leaves record
        remaining_leaves = await db.execute(
            select(RemainingLeaves)
            .where(
                RemainingLeaves.leave_detail_id == leave_detail.id,
                RemainingLeaves.year == datetime.now().year
            )
        )
        remaining_leaves = remaining_leaves.scalars().first()

        if not remaining_leaves:
            raise ValueError(f"No remaining leaves record found for employee {employee_id}")

        # 3. Update the remaining leaves balance
        if remaining_leaves.remaining_leaves < days_applied:
            raise ValueError("Not enough remaining leaves")

        remaining_leaves.remaining_leaves -= days_applied
        
        if clear_lop:
            # Here you would add logic to clear LOP days
            # This depends on how you track LOP in your system
            pass

        await db.commit()
        await db.refresh(remaining_leaves)
        
        return remaining_leaves

    except Exception as e:
        await db.rollback()
        raise e