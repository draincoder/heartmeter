from dataclasses import dataclass

from reporter.domain.models import Measurement, User


@dataclass
class Report:
    payload: bytes
    format: str
    filename: str


@dataclass
class History:
    user: User
    data: list[Measurement]
