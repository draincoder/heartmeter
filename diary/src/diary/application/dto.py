from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True, frozen=True)
class NewUserDTO:
    name: str
    email: str
    timezone: str
    birthday: datetime


@dataclass(slots=True, frozen=True)
class UpdateUserDTO(NewUserDTO):
    id: UUID


@dataclass(slots=True, frozen=True)
class NewMeasurementDTO:
    user_id: UUID
    systolic: int
    diastolic: int
    pulse: int
    drug: str
    note: str
    date: datetime


@dataclass(slots=True, frozen=True)
class UpdateMeasurementDTO(NewMeasurementDTO):
    id: UUID
