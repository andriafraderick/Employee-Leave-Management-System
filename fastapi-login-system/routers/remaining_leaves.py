from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import get_db
from schemas import RemainingLeaveCreate, RemainingLeaveUpdate, RemainingLeavesOut
from crud.remaining_leaves import create_remaining_leave, update_remaining_leave, get_leave_detail_id

router = APIRouter()

@router.post("/", response_model=RemainingLeavesOut)
async def create_or_update_remaining_leave(
    rem: RemainingLeaveCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        # First try to find existing record
        leave_detail_id = await get_leave_detail_id(db, rem.employee_id, rem.leave_type)
        if not leave_detail_id:
            raise HTTPException(
                status_code=404,
                detail=f"No leave details found for employee {rem.employee_id} and type {rem.leave_type}"
            )

        # Try to update existing record
        updated = await update_remaining_leave(
            db,
            leave_detail_id=leave_detail_id,
            rem=RemainingLeaveUpdate(
                remaining_leaves=rem.remaining_leaves,
                total_leaves=rem.total_leaves
            )
        )
        
        # If no record exists, create new one
        if not updated:
            return await create_remaining_leave(db, rem)
            
        return updated
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )