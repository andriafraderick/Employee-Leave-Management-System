import os
from uuid import uuid4
from fastapi import UploadFile
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from models import student_details
from schemas import StudentBase

UPLOAD_DIR = "uploaded_dobs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def create_student(student_data: StudentBase, dob_file: UploadFile, db: AsyncSession):
    file_ext = dob_file.filename.split('.')[-1]
    file_name = f"{uuid4()}.{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, file_name)

    with open(file_path, "wb") as f:
        content = await dob_file.read()
        f.write(content)

    query = insert(student_details).values(
        name=student_data.name,
        roll_no=student_data.roll_no,
        **{"class": student_data.class_},
        gender=student_data.gender,
        email_id=student_data.email_id,
        dob_file_path=file_path
    )

    await db.execute(query)
    await db.commit()

    result = await db.execute(
        select(student_details).where(student_details.c.roll_no == student_data.roll_no)
    )
    return result.fetchone()

async def get_student_by_name_and_roll(name: str, roll_no: str, db: AsyncSession):
    result = await db.execute(
        select(student_details).where(
            (student_details.c.name == name) &
            (student_details.c.roll_no == roll_no)
        )
    )
    return result.scalar_one_or_none()
