from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class User:
    id: UUID
    name: str
    email: str
    timezone: str
    birthday: datetime
    created_at: datetime
    updated_at: datetime


@dataclass
class Measurement:
    id: UUID
    user_id: UUID
    systolic: int
    diastolic: int
    pulse: int
    drug: str
    note: str
    date: datetime
    created_at: datetime
    updated_at: datetime
