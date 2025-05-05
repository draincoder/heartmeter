from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from diary.application.dto import NewMeasurementDTO, NewUserDTO, UpdateMeasurementDTO, UpdateUserDTO


class MeasurementBody(BaseModel):
    systolic: int
    diastolic: int
    pulse: int
    drug: str
    note: str
    date: datetime

    def to_new_dto(self, user_id: UUID) -> NewMeasurementDTO:
        return NewMeasurementDTO(
            user_id=user_id,
            systolic=self.systolic,
            diastolic=self.diastolic,
            pulse=self.pulse,
            drug=self.drug,
            note=self.note,
            date=self.date,
        )

    def to_update_dto(self, user_id: UUID, measurement_id: UUID) -> UpdateMeasurementDTO:
        return UpdateMeasurementDTO(
            id=measurement_id,
            user_id=user_id,
            systolic=self.systolic,
            diastolic=self.diastolic,
            pulse=self.pulse,
            drug=self.drug,
            note=self.note,
            date=self.date,
        )


class UserBody(BaseModel):
    name: str
    email: str
    timezone: str
    birthday: datetime

    def to_new_dto(self) -> NewUserDTO:
        return NewUserDTO(
            name=self.name,
            email=self.email,
            timezone=self.timezone,
            birthday=self.birthday,
        )

    def to_update_dto(self, user_id: UUID) -> UpdateUserDTO:
        return UpdateUserDTO(
            id=user_id,
            name=self.name,
            email=self.email,
            timezone=self.timezone,
            birthday=self.birthday,
        )
