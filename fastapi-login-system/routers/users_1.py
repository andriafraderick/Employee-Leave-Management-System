from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from passlib.context import CryptContext

from schemas import UserCreate, UserLogin, UserOut
from config.db import async_session
from crud import users_1 as crud_users
from fastapi import APIRouter, Depends
from auth.auth import get_current_user

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dependency
async def get_db():
    async with async_session() as session:
        yield session

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await crud_users.create_user(user, db, pwd_context)

@router.post("/login")
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    return await crud_users.login_user(user, db, pwd_context)

@router.get("/users/", response_model=List[UserOut])
async def get_users(db: AsyncSession = Depends(get_db)):
    return await crud_users.get_all_users(db)

@router.get("/users/{user_id}", response_model=UserOut)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await crud_users.get_user_by_id(user_id, db)

@router.put("/users/{user_id}", response_model=UserOut)
async def update_user(user_id: int, user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await crud_users.update_user(user_id, user, db, pwd_context)

@router.patch("/users/{user_id}", response_model=UserOut)
async def patch_user(user_id: int, partial_data: dict, db: AsyncSession = Depends(get_db)):
    return await crud_users.patch_user(user_id, partial_data, db, pwd_context)

@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await crud_users.delete_user(user_id, db)

router = APIRouter()

@router.get("/protected")
def protected_route(user = Depends(get_current_user)):
    return {"message": "You're authorized!", "user": user}

