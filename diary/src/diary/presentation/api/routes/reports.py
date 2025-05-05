from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from diary.application.report import RequestReportInteractor
from diary.presentation.api.depends import UserID
from diary.presentation.api.models import SuccessResponse

reports_router = APIRouter(
    prefix="/reports",
    tags=["Report"],
    include_in_schema=True,
    route_class=DishkaRoute,
)


@reports_router.post("/generate")
async def create_measurement(
    user_id: UserID,
    interactor: FromDishka[RequestReportInteractor],
) -> SuccessResponse:
    await interactor.request(user_id)
    return SuccessResponse(message="The report will be generated and sent to your email")
