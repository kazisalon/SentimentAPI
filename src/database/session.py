from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
import os

# 1. DATABASE URL
# For local dev, we use SQLite. 
# FOR PRODUCTION (PostgreSQL), you would change this to:
# "postgresql+asyncpg://username:password@localhost:5432/sentiment_db"
DATABASE_URL = "sqlite+aiosqlite:///./sentiment.db"

# 2. Create the Async Engine
engine = create_async_engine(
    DATABASE_URL, 
    echo=False, # Set to True to see raw SQL queries in the console (great for debugging)
    future=True
)

# 3. Create a Session Factory
AsyncSessionLocal = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# 4. Dependency Injection for FastAPI
async def get_db() -> AsyncSession:
    """
    FastAPI dependency that provides a database session.
    It ensures the session is properly closed after the request is done.
 is done.
    """
    async with AsyncSessionLocal() as session:
        yield session