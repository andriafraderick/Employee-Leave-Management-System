from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from auth.jwt import verify_token
from config.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from sqlalchemy import select

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_token(token)
        if payload is None:
            raise credentials_exception

        employee_id = payload.get("employee_id")
        if employee_id is None:
            raise credentials_exception

        # Fetch full user from DB using employee_id
        result = await db.execute(
            select(User).where(User.employee_id == employee_id)
        )
        user = result.scalar_one_or_none()
        if user is None:
            raise credentials_exception
        return user  # return full SQLAlchemy user object

    except JWTError:
        raise credentials_exception