from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from sqlalchemy.orm import DeclarativeBase

from config import DATABASE_URL

class Base(DeclarativeBase):
    pass

engine = create_async_engine(DATABASE_URL)

async def get_session():
    async with AsyncSession(engine) as session:
        yield session
