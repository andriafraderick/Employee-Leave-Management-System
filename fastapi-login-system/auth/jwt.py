from datetime import datetime, timedelta
from jose import JWTError, jwt

from schemas import TokenData

SECRET_KEY = "1234567890poiuytrewq0987654321asdfghjkl"  # TODO: Replace with os.getenv("SECRET_KEY") using dotenv
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> TokenData | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenData(**payload)
    except JWTError:
        return None


# ---------- auth/password_utils.py ----------
from passlib.context import CryptContext
from passlib.exc import UnknownHashError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except UnknownHashError:
        return False

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# ---------- routers/token.py ----------
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models import User
from auth.jwt import create_access_token, create_refresh_token
from auth.password_utils import verify_password
from schemas import Token
from config.db import async_session

router = APIRouter()

async def get_db() -> AsyncSession: # type: ignore
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

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_info": {
            "employee_id": user.employee_id,
            "name": user.name,
            "role": user.role
        },
        "refresh_token": refresh_token,
        "role": user.role
    }