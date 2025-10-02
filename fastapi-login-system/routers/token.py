from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import User
from auth.jwt import create_access_token, create_refresh_token
from auth.password_utils import verify_password
from schemas import Token, UserInfo
from config.db import async_session

router = APIRouter()

# ✅ Database dependency
async def get_db() -> AsyncSession:  # type: ignore
    async with async_session() as session:
        yield session

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalars().first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token({
        "sub": user.email,
        "role": user.role.value,
        "employee_id": user.employee_id
    })

    refresh_token = create_refresh_token({
        "sub": user.email,
        "role": user.role.value,
        "employee_id": user.employee_id
    })

    return Token(
    access_token=access_token,
    token_type="bearer",
    refresh_token=refresh_token,
    role=user.role.value,
    user_info=UserInfo(
        employee_id=user.employee_id,
        name=user.name,
        role=user.role.value
    )
)
