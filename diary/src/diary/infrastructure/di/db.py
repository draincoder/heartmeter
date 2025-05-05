from typing import AsyncIterable

from dishka import AnyOf, Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, close_all_sessions

from diary.application.interfaces import MeasurementReader, MeasurementWriter, TXManager, UserReader, UserWriter
from diary.infrastructure.db.config import PGConfig
from diary.infrastructure.db.factory import create_engine, create_session_maker
from diary.infrastructure.db.gateways import MeasurementGateway, UserGateway


class DBProvider(Provider):
    def __init__(self, config: PGConfig) -> None:
        super().__init__()
        self._config = config

    @provide(scope=Scope.APP)
    async def get_pg_engine(self) -> AsyncIterable[AsyncEngine]:
        engine = create_engine(self._config)
        yield engine
        await engine.dispose(close=True)
        await close_all_sessions()

    @provide(scope=Scope.APP)
    async def get_pg_pool(self, pg_engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return create_session_maker(pg_engine)

    @provide(scope=Scope.REQUEST)
    async def get_pg_session(
        self,
        pool: async_sessionmaker[AsyncSession],
    ) -> AnyOf[AsyncIterable[TXManager], AsyncIterable[AsyncSession]]:
        async with pool() as session:
            yield session

    user_gateway = provide(
        UserGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[UserReader, UserWriter],
    )
    measurement_gateway = provide(
        MeasurementGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[MeasurementReader, MeasurementWriter],
    )
