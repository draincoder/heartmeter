from abc import abstractmethod
from datetime import datetime
from typing import Protocol
from uuid import UUID

from diary.domain.models import Measurement, User


class UserReader(Protocol):
    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User | None: ...

    @abstractmethod
    async def email_exists(self, email: str) -> bool: ...


class UserWriter(Protocol):
    @abstractmethod
    async def save(self, user: User) -> None: ...


class MeasurementReader(Protocol):
    @abstractmethod
    async def get_by_id(self, user_id: UUID, measurement_id: UUID) -> Measurement | None: ...

    @abstractmethod
    async def get_all_by_user_id(self, user_id: UUID) -> list[Measurement]: ...


class MeasurementWriter(Protocol):
    @abstractmethod
    async def save(self, measurement: Measurement) -> None: ...

    @abstractmethod
    async def delete(self, measurement_id: UUID) -> None: ...


class TXManager(Protocol):
    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def flush(self) -> None: ...


class UUIDGenerator(Protocol):
    def __call__(self) -> UUID: ...


class TimeGenerator(Protocol):
    def __call__(self) -> datetime: ...
