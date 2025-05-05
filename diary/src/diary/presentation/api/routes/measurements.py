from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, HTTPException
from starlette import status

from diary.application.measurement import (
    CreateMeasurementInteractor,
    DeleteMeasurementInteractor,
    GetMeasurementInteractor,
    UpdateMeasurementInteractor,
)
from diary.domain.models import Measurement
from diary.presentation.api.depends import UserID
from diary.presentation.api.models import MeasurementBody, SuccessListResponse, SuccessResponse

measurements_router = APIRouter(
    prefix="/measurements",
    tags=["Measurement"],
    include_in_schema=True,
    route_class=DishkaRoute,
)


@measurements_router.post("")
async def create_measurement(
    user_id: UserID,
    body: MeasurementBody,
    interactor: FromDishka[CreateMeasurementInteractor],
) -> SuccessResponse[Measurement]:
    result = await interactor.create(body.to_new_dto(user_id))
    return SuccessResponse(data=result)


@measurements_router.get("")
async def get_all_measurements(
    user_id: UserID,
    interactor: FromDishka[GetMeasurementInteractor],
) -> SuccessListResponse[Measurement]:
    result = await interactor.get_all(user_id)
    return SuccessListResponse(data=result)


@measurements_router.get("/{measurement_id}")
async def get_measurement(
    measurement_id: UUID,
    user_id: UserID,
    interactor: FromDishka[GetMeasurementInteractor],
) -> SuccessResponse[Measurement]:
    result = await interactor.get(user_id, measurement_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Measurement not found")

    return SuccessResponse(data=result)


@measurements_router.put("/{measurement_id}")
async def update_measurement(
    measurement_id: UUID,
    user_id: UserID,
    body: MeasurementBody,
    interactor: FromDishka[UpdateMeasurementInteractor],
) -> SuccessResponse[Measurement]:
    result = await interactor.update(body.to_update_dto(user_id, measurement_id))
    return SuccessResponse(data=result)


@measurements_router.delete("/{measurement_id}")
async def delete_measurement(
    measurement_id: UUID,
    user_id: UserID,
    interactor: FromDishka[DeleteMeasurementInteractor],
) -> SuccessResponse:
    await interactor.delete(user_id, measurement_id)
    return SuccessResponse()
