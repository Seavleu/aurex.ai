"""
AUREX.AI - Database Connection Manager.

This module provides database connection pooling and session management
for PostgreSQL with async support.
"""

import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from dotenv import load_dotenv
from loguru import logger
from sqlalchemy import create_engine, pool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

# Load environment variables from .env file
load_dotenv()

# Base class for ORM models
Base = declarative_base()

# Database URL from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://aurex:aurex_password@localhost:5432/aurex_db",
)

# Sync database URL (for migrations)
SYNC_DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")


class DatabaseManager:
    """Manages database connections and sessions."""

    def __init__(self, database_url: str = DATABASE_URL) -> None:
        """
        Initialize database manager.

        Args:
            database_url: Database connection string
        """
        self.database_url = database_url
        self._engine = None
        self._session_factory = None
        self._sync_engine = None
        self._sync_session_factory = None
        logger.info("Database manager initialized")

    def get_async_engine(self):
        """Get or create async database engine."""
        if self._engine is None:
            self._engine = create_async_engine(
                self.database_url,
                echo=False,
                pool_size=20,
                max_overflow=0,
                pool_pre_ping=True,
                pool_recycle=3600,
            )
            logger.info("Async database engine created")
        return self._engine

    def get_sync_engine(self):
        """Get or create sync database engine (for migrations)."""
        if self._sync_engine is None:
            self._sync_engine = create_engine(
                SYNC_DATABASE_URL,
                echo=False,
                poolclass=pool.QueuePool,
                pool_size=10,
                max_overflow=5,
                pool_pre_ping=True,
            )
            logger.info("Sync database engine created")
        return self._sync_engine

    def get_async_session_factory(self) -> async_sessionmaker:
        """Get async session factory."""
        if self._session_factory is None:
            engine = self.get_async_engine()
            self._session_factory = async_sessionmaker(
                engine,
                class_=AsyncSession,
                expire_on_commit=False,
            )
            logger.info("Async session factory created")
        return self._session_factory

    def get_sync_session_factory(self) -> sessionmaker:
        """Get sync session factory."""
        if self._sync_session_factory is None:
            engine = self.get_sync_engine()
            self._sync_session_factory = sessionmaker(
                engine,
                class_=Session,
                expire_on_commit=False,
            )
            logger.info("Sync session factory created")
        return self._sync_session_factory

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Get async database session context manager.

        Yields:
            AsyncSession: Database session

        Example:
            async with db_manager.get_session() as session:
                result = await session.execute(query)
        """
        session_factory = self.get_async_session_factory()
        session = session_factory()
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            await session.close()

    async def close(self) -> None:
        """Close database connections."""
        if self._engine is not None:
            await self._engine.dispose()
            logger.info("Async database engine disposed")

    async def health_check(self) -> bool:
        """
        Check database connectivity.

        Returns:
            bool: True if database is accessible
        """
        try:
            async with self.get_session() as session:
                await session.execute("SELECT 1")
            logger.info("Database health check: OK")
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False


# Global database manager instance
db_manager = DatabaseManager()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for FastAPI to get database session.

    Yields:
        AsyncSession: Database session

    Example:
        @app.get("/users")
        async def get_users(session: AsyncSession = Depends(get_db_session)):
            result = await session.execute(select(User))
            return result.scalars().all()
    """
    async with db_manager.get_session() as session:
        yield session


async def init_database() -> None:
    """Initialize database schema (creates all tables)."""
    engine = db_manager.get_async_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database schema initialized")


async def close_database() -> None:
    """Close all database connections."""
    await db_manager.close()
    logger.info("Database connections closed")

