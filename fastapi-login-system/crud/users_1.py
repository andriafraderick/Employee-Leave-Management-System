from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import UserCreate, UserLogin
from models import users_1
from passlib.context import CryptContext

async def create_user(user: UserCreate, db: AsyncSession, pwd_context: CryptContext):
    result = await db.execute(users_1.select().where(users_1.c.username == user.username))
    if result.scalar():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    
    hashed_password = pwd_context.hash(user.password)
    query = users_1.insert().values(username=user.username, password=hashed_password)
    await db.execute(query)
    await db.commit()
    result = await db.execute(users_1.select().where(users_1.c.username == user.username))
    return result.fetchone()

# This function handles the login logic for a user.
# It takes in the user's login data (username and password),
# the database session (db), and the password hashing context (pwd_context).
async def login_user(user: UserLogin, db: AsyncSession, pwd_context: CryptContext):
    result = await db.execute(users_1.select().where(users_1.c.username == user.username))
    db_user = result.fetchone()
    if not db_user or not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"message": "Login successful"}

async def get_all_users(db: AsyncSession):
    result = await db.execute(users_1.select())
    return result.fetchall()

# SELECT * FROM users WHERE id = user_id
async def get_user_by_id(user_id: int, db: AsyncSession):
    result = await db.execute(users_1.select().where(users_1.c.id == user_id))
     # Returns a single user (or None if not found)
    return result.fetchone()

async def update_user(user_id: int, user_data: UserCreate, db: AsyncSession, pwd_context: CryptContext):
    # Hash the new password before storing it
    hashed_password = pwd_context.hash(user_data.password)
    # Prepare UPDATE query with the new data
    query = users_1.update().where(users_1.c.id == user_id).values(
        username=user_data.username,
        password=hashed_password
    )
    await db.execute(query)
    await db.commit()
    return await get_user_by_id(user_id, db)

async def patch_user(user_id: int, partial_data: dict, db: AsyncSession, pwd_context: CryptContext):
    if "password" in partial_data:
        partial_data["password"] = pwd_context.hash(partial_data["password"])
    query = users_1.update().where(users_1.c.id == user_id).values(**partial_data)
    await db.execute(query)
    await db.commit()
    return await get_user_by_id(user_id, db)

async def delete_user(user_id: int, db: AsyncSession):
    query = users_1.delete().where(users_1.c.id == user_id)
    await db.execute(query)
    await db.commit()
    return {"message": f"User with ID {user_id} deleted"}

async def authenticate_user(username: str, password: str, db: AsyncSession, pwd_context: CryptContext):
    result = await db.execute(users_1.select().where(users_1.c.username == username))
    db_user = result.fetchone()
    if not db_user:
        return None
    if not pwd_context.verify(password, db_user.password):
        return None
    return db_user

