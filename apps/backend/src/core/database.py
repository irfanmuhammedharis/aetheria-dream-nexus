# Verified against Phase 1/2: Async SQLAlchemy + Postgres setup

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:password@localhost:5432/aetheria_db")

# Async engine for Postgres using asyncpg
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# Dependency for FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# Verification Log
# - Uses Postgres via asyncpg (recommended for FastAPI async IO).
# - DATABASE_URL must be provided via env for production (we default for local dev).
# - Chosen approach aligns with Section 1.2 and Phase 1 plumbing requirements.