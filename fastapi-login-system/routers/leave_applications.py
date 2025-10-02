from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import get_db
from models import LeaveApplications
from auth.auth import get_current_user
from sqlalchemy import select
from crud.leave_applications import create_leave_application

router = APIRouter(prefix="/leave_applications", tags=["Leave Applications"])

@router.get("/")
async def get_user_leave_applications(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all leave applications for the current user
    """
    result = await db.execute(
        select(LeaveApplications).where(LeaveApplications.employee_id == current_user["employee_id"])
    )
    applications = result.scalars().all()
    return applications

@router.post("/")
async def create_leave_application_endpoint(
    employee_id: str = Form(...),
    leave_type_id: int = Form(...),
    start_date: str = Form(...),
    end_date: str = Form(...),
    manager_id: str = Form(...),
    total_days: float = Form(...),
    status: str = Form(...),
    reason: str = Form(...),
    number_of_files: int = Form(...),
    reason_if_rejected: str = Form(None),
    file: UploadFile = File(None),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new leave application
    """
    # Verify the employee_id matches the current user
    if employee_id != current_user["employee_id"]:
        raise HTTPException(
            status_code=403,
            detail="You can only create leave applications for yourself"
        )

    data = {
        "employee_id": employee_id,
        "leave_type_id": leave_type_id,
        "start_date": start_date,
        "end_date": end_date,
        "manager_id": manager_id,
        "total_days": total_days,
        "status": status,
        "reason": reason,
        "number_of_files": number_of_files,
        "reason_if_rejected": reason_if_rejected,
    }

    return await create_leave_application(db, data, file)