from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, HTTPException
from starlette import status

from diary.application.user import (
    CreateUserInteractor,
    GetUserInteractor,
    UpdateUserInteractor,
)
from diary.domain.models import User
from diary.presentation.api.models import SuccessResponse, UserBody

users_router = APIRouter(
    prefix="/users",
    tags=["User"],
    include_in_schema=True,
    route_class=DishkaRoute,
)


@users_router.post("")
async def create_user(
    body: UserBody,
    interactor: FromDishka[CreateUserInteractor],
) -> SuccessResponse[User]:
    result = await interactor.create(body.to_new_dto())
    return SuccessResponse(data=result)


@users_router.get("/{user_id}")
async def get_user(
    user_id: UUID,
    interactor: FromDishka[GetUserInteractor],
) -> SuccessResponse[User]:
    result = await interactor.get(user_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return SuccessResponse(data=result)


@users_router.put("/{user_id}")
async def update_user(
    user_id: UUID,
    body: UserBody,
    interactor: FromDishka[UpdateUserInteractor],
) -> SuccessResponse[User]:
    result = await interactor.update(body.to_update_dto(user_id))
    return SuccessResponse(data=result)
