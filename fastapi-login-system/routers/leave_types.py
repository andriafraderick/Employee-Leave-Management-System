from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import get_db
from schemas import LeaveTypeCreate
from crud.leave_types import create_leave_type

router = APIRouter()

@router.post("/leave-types")
async def create_leave_type_endpoint(
    leave_type: LeaveTypeCreate,
    db: AsyncSession = Depends(get_db)
):
    return await create_leave_type(db, leave_type)
