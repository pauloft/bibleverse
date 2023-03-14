from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Create a SQLite engine
sqlite_url = "sqlite+aiosqlite:///bible.db"
engine = create_async_engine(sqlite_url)


# function to create the database using the table
# models if it does not exist
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


# get_session used in dependency injection
async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
