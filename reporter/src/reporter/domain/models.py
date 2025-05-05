from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class User:
    id: UUID
    email: str
    name: str


@dataclass
class Measurement:
    systolic: int
    diastolic: int
    pulse: int
    drug: str
    note: str
    date: datetime
