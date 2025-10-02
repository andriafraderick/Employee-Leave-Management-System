from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import LeaveApplyRequest
from crud.leave_operations import apply_leave_and_update_balance
from config.db import get_db

router = APIRouter()

@router.post("/apply-leave")
async def apply_leave(
    request: LeaveApplyRequest,
    db: AsyncSession = Depends(get_db)
):
    try:
        result = await apply_leave_and_update_balance(
            db,
            employee_id=request.employee_id,
            days_applied=request.days_applied,
            leave_type=request.leave_type,
            clear_lop=request.clear_lop
        )
        
        return {
            "message": "Leave applied successfully",
            "remaining_leaves": result.remaining_leaves,
            "total_leaves": result.total_leaves
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))