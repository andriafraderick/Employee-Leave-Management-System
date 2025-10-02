from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

# ✅ DB URL
DATABASE_URL = "postgresql+asyncpg://admin_user:123andria890@localhost/admin_db"

# ✅ Engine and Session
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
metadata = MetaData()
Base = declarative_base()

# ✅ Use directly in Depends()
async def get_db():
    async with async_session() as session:
        yield session
