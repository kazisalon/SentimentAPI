import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# Load environment variables from .env file
load_dotenv()

# Fallback to SQLite if DATABASE_URL is not set (good for local testing without Docker)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./sentiment.db")

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session