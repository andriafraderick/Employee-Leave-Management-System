from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import async_session
from schemas import StudentBase, StudentOut
from crud import students as crud_students
from auth.auth import get_current_user

router = APIRouter()

async def get_db():
    async with async_session() as session:
        yield session

@router.post("/students/", response_model=StudentOut)
async def add_student(
    name: str = Form(...),
    roll_no: str = Form(...),
    class_: str = Form(...),
    gender: str = Form(...),
    email_id: str = Form(...),
    dob_file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    student_data = StudentBase(**{
        "name": name,
        "roll_no": roll_no,
        "class": class_,
        "gender": gender,
        "email_id": email_id
    })
    return await crud_students.create_student(student_data, dob_file, db)
