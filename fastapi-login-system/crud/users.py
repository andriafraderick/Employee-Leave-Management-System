from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from schemas import UserCreate
from auth.password_utils import get_password_hash  # ✅ Import

async def create_user(db: AsyncSession, user: UserCreate):
    print("Received user data:", user.dict())  # Debug 1

    # ✅ Hash the password before saving
    user_dict = user.dict()
    user_dict["password"] = get_password_hash(user_dict["password"])

    db_user = User(**user_dict)
    print("User model instance created:", db_user)  # Debug 2

    db.add(db_user)
    print("User added to the session.")  # Debug 3

    await db.commit()
    print("Transaction committed.")  # Debug 4

    await db.refresh(db_user)
    print("Session refreshed. Final user instance:", db_user)  # Debug 5

    return db_user
