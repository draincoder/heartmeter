import logging
from uuid import UUID

from diary.application.interfaces import MeasurementReader, MeasurementWriter, TimeGenerator, TXManager, UUIDGenerator
from diary.domain.models import Measurement
from .dto import NewMeasurementDTO, UpdateMeasurementDTO
from .exceptions import MeasurementNotFoundError

logger = logging.getLogger(__name__)


class GetMeasurementInteractor:
    def __init__(self, measurement_reader: MeasurementReader) -> None:
        self._measurement_reader = measurement_reader

    async def get(self, user_id: UUID, measurement_id: UUID) -> Measurement | None:
        return await self._measurement_reader.get_by_id(user_id, measurement_id)

    async def get_all(self, user_id: UUID) -> list[Measurement]:
        return await self._measurement_reader.get_all_by_user_id(user_id)


class CreateMeasurementInteractor:
    def __init__(
        self,
        measurement_writer: MeasurementWriter,
        uuid_generator: UUIDGenerator,
        time_generator: TimeGenerator,
        tx: TXManager,
    ) -> None:
        self._measurement_writer = measurement_writer
        self._uuid_generator = uuid_generator
        self._time_generator = time_generator
        self._tx = tx

    async def create(self, measurement: NewMeasurementDTO) -> Measurement:
        now = self._time_generator()
        new_id = self._uuid_generator()
        new_measurement = Measurement(
            id=new_id,
            user_id=measurement.user_id,
            diastolic=measurement.diastolic,
            systolic=measurement.systolic,
            pulse=measurement.pulse,
            drug=measurement.drug,
            note=measurement.note,
            date=measurement.date,
            created_at=now,
            updated_at=now,
        )

        await self._measurement_writer.save(new_measurement)
        await self._tx.commit()
        logger.info(f"Created measurement {new_measurement.id} by {new_measurement.user_id}")
        return new_measurement


class UpdateMeasurementInteractor:
    def __init__(
        self,
        measurement_reader: MeasurementReader,
        measurement_writer: MeasurementWriter,
        time_generator: TimeGenerator,
        tx: TXManager,
    ) -> None:
        self._measurement_reader = measurement_reader
        self._measurement_writer = measurement_writer
        self._time_generator = time_generator
        self._tx = tx

    async def update(self, measurement: UpdateMeasurementDTO) -> Measurement:
        exist_measurement = await self._measurement_reader.get_by_id(measurement.user_id, measurement.id)
        if exist_measurement is None:
            raise MeasurementNotFoundError(measurement.id)

        now = self._time_generator()
        updated_measurement = Measurement(
            id=exist_measurement.id,
            user_id=exist_measurement.user_id,
            diastolic=measurement.diastolic,
            systolic=measurement.systolic,
            pulse=measurement.pulse,
            drug=measurement.drug,
            note=measurement.note,
            date=measurement.date,
            created_at=exist_measurement.created_at,
            updated_at=now,
        )

        await self._measurement_writer.save(updated_measurement)
        await self._tx.commit()
        logger.info(f"Updated measurement {measurement.id} by {measurement.user_id}")
        return updated_measurement


class DeleteMeasurementInteractor:
    def __init__(
        self,
        measurement_reader: MeasurementReader,
        measurement_writer: MeasurementWriter,
        tx: TXManager,
    ) -> None:
        self._measurement_reader = measurement_reader
        self._measurement_writer = measurement_writer
        self._tx = tx

    async def delete(self, user_id: UUID, measurement_id: UUID) -> None:
        exist_measurement = await self._measurement_reader.get_by_id(user_id, measurement_id)
        if exist_measurement is None:
            raise MeasurementNotFoundError(measurement_id)

        await self._measurement_writer.delete(measurement_id)
        logger.info(f"Deleted measurement {measurement_id} by {measurement_id}")
        await self._tx.commit()
