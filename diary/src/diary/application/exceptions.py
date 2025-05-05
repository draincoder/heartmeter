from dataclasses import dataclass
from uuid import UUID


class ApplicationError(Exception):
    @property
    def message(self) -> str:
        return "An application error occurred"


@dataclass(slots=True, frozen=True)
class EmailAlreadyExistsError(ApplicationError):
    email: str

    @property
    def message(self) -> str:
        return f"User with email '{self.email}' already exists"


@dataclass(slots=True, frozen=True)
class NotFoundError(Exception):
    @property
    def message(self) -> str:
        return "Not found"


@dataclass(slots=True, frozen=True)
class UserNotFoundError(NotFoundError):
    user_id: UUID

    @property
    def message(self) -> str:
        return f"User with id '{self.user_id}' not found"


@dataclass(slots=True, frozen=True)
class MeasurementNotFoundError(NotFoundError):
    measurement_id: UUID

    @property
    def message(self) -> str:
        return f"Measurement with id '{self.measurement_id}' not found"
