from uuid import UUID

from sqlalchemy import ScalarResult, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from diary.application.interfaces import MeasurementReader, MeasurementWriter, UserReader, UserWriter
from diary.domain.models import Measurement, User


class UserGateway(UserReader, UserWriter):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, user_id: UUID) -> User | None:
        stmt = select(User).where(User.id == user_id)  # type: ignore[arg-type]
        result: User | None = await self._session.scalar(stmt)
        return result

    async def email_exists(self, email: str) -> bool:
        stmt = select(User).where(User.email == email)  # type: ignore[arg-type]
        result = await self._session.scalar(stmt)
        return bool(result)

    async def save(self, user: User) -> None:
        await self._session.merge(user)


class MeasurementGateway(MeasurementReader, MeasurementWriter):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, user_id: UUID, measurement_id: UUID) -> Measurement | None:
        stmt = select(Measurement).where(Measurement.user_id == user_id).where(Measurement.id == measurement_id)  # type: ignore[arg-type]
        result: Measurement | None = await self._session.scalar(stmt)
        return result

    async def get_all_by_user_id(self, user_id: UUID) -> list[Measurement]:
        stmt = select(Measurement).where(Measurement.user_id == user_id)  # type: ignore[arg-type]
        result: ScalarResult[Measurement] = await self._session.scalars(stmt)
        return result.all()  # type: ignore[return-value]

    async def save(self, measurement: Measurement) -> None:
        await self._session.merge(measurement)

    async def delete(self, measurement_id: UUID) -> None:
        stmt = delete(Measurement).where(Measurement.id == measurement_id)  # type: ignore[arg-type]
        await self._session.execute(stmt)
