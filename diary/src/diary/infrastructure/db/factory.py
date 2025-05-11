from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from sqlalchemy import make_url
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from .config import PGConfig


def create_engine(config: PGConfig) -> AsyncEngine:
    engine = create_async_engine(url=make_url(config.uri), echo=config.echo)
    SQLAlchemyInstrumentor().instrument(engine=engine.sync_engine)
    return engine


def create_session_maker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)
