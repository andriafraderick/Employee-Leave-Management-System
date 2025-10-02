from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import get_db
from schemas import LeaveDetailCreate
from crud.leave_details import create_leave_detail

router = APIRouter()

@router.post("/leave-details")
async def create_leave_detail_endpoint(
    detail: LeaveDetailCreate,
    db: AsyncSession = Depends(get_db)
):
    return await create_leave_detail(db, detail)
