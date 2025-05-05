from datetime import UTC, datetime
from uuid import uuid4

from dishka import Provider, Scope, provide

from diary.application.interfaces import TimeGenerator, UUIDGenerator
from diary.application.measurement import (
    CreateMeasurementInteractor,
    DeleteMeasurementInteractor,
    GetMeasurementInteractor,
    UpdateMeasurementInteractor,
)
from diary.application.user import CreateUserInteractor, GetUserInteractor, UpdateUserInteractor


class InteractorProvider(Provider):
    @provide(scope=Scope.APP)
    def get_uuid_generator(self) -> UUIDGenerator:
        return uuid4

    @provide(scope=Scope.APP)
    def get_time_generator(self) -> TimeGenerator:
        return lambda: datetime.now(tz=UTC)

    get_user_interactor = provide(GetUserInteractor, scope=Scope.REQUEST)
    create_user_interactor = provide(CreateUserInteractor, scope=Scope.REQUEST)
    update_user_interactor = provide(UpdateUserInteractor, scope=Scope.REQUEST)

    get_measurement_interactor = provide(GetMeasurementInteractor, scope=Scope.REQUEST)
    create_measurement_interactor = provide(CreateMeasurementInteractor, scope=Scope.REQUEST)
    update_measurement_interactor = provide(UpdateMeasurementInteractor, scope=Scope.REQUEST)
    delete_measurement_interactor = provide(DeleteMeasurementInteractor, scope=Scope.REQUEST)
