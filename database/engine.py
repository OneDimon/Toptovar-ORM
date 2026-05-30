"""Единая точка конфигурации БД для всего проекта.

Меняешь DB_URL в .env — работает любая БД поддерживаемая SQLAlchemy.
Меняешь реализацию репозитория — handlers не трогаешь вообще.
"""
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL", "postgresql+asyncpg://postgres:password@localhost:5432/botTovar")

engine = create_async_engine(
    DB_URL,
    echo=False,        # True для отладки SQL
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
)

AsyncSessionFactory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Базовый класс для всех ORM-моделей."""
    pass


async def get_session() -> AsyncSession:
    """Dependency для получения сессии (используется в репозиториях)."""
    async with AsyncSessionFactory() as session:
        yield session
