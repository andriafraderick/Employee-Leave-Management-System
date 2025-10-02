from sqlalchemy.ext.asyncio import AsyncSession
from models import LeaveApplications
import shutil
import os
from datetime import datetime
from fastapi import UploadFile

UPLOAD_DIR = "uploaded_files"

async def create_leave_application(db: AsyncSession, data: dict, file: UploadFile = None):
    file_path = None

    # Save uploaded file if present
    if file:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_path = file_location

    # Parse date fields if needed
    start_date = datetime.fromisoformat(data["start_date"])
    end_date = datetime.fromisoformat(data["end_date"])
    date_of_application = datetime.now()

    db_app = LeaveApplications(
        employee_id=data["employee_id"],
        leave_type_id=data["leave_type_id"],
        start_date=start_date,
        end_date=end_date,
        manager_id=data["manager_id"],
        total_days=data["total_days"],
        status=data["status"],
        reason=data["reason"],
        file_path=file_path,
        number_of_files=data["number_of_files"],
        reason_if_rejected=data.get("reason_if_rejected"),
        date_of_application=date_of_application
    )

    db.add(db_app)
    await db.commit()
    await db.refresh(db_app)
    return db_app
