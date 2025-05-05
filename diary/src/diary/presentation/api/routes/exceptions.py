import logging

from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from pydantic_core import ValidationError
from starlette import status
from starlette.requests import Request

from diary.application.exceptions import ApplicationError, EmailAlreadyExistsError, NotFoundError
from diary.presentation.api.models import ErrorResponse, ValidationData, ValidationErrorResponse

logger = logging.getLogger(__name__)


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ValidationError, validation_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(HTTPException, api_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(EmailAlreadyExistsError, app_conflict_handler)  # type: ignore[arg-type]
    app.add_exception_handler(NotFoundError, not_found_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(ApplicationError, app_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(Exception, unknown_exception_handler)


async def validation_exception_handler(
    _: Request,
    err: ValidationError | RequestValidationError,
) -> ORJSONResponse:
    response = ValidationErrorResponse()

    for e in err.errors():
        message = e["msg"].replace("Value error, ", "")
        location = e["loc"]
        response.errors.append(ValidationData(message=message, location=location))

    return ORJSONResponse(jsonable_encoder(response), status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


async def api_exception_handler(request: Request, err: HTTPException) -> ORJSONResponse:
    return await handle_error(request, err, err.detail, err.status_code)


async def app_conflict_handler(request: Request, err: EmailAlreadyExistsError) -> ORJSONResponse:
    return await handle_error(request, err, err.message, status.HTTP_409_CONFLICT)


async def not_found_exception_handler(request: Request, err: NotFoundError) -> ORJSONResponse:
    return await handle_error(request, err, err.message, status.HTTP_404_NOT_FOUND)


async def app_exception_handler(request: Request, err: ApplicationError) -> ORJSONResponse:
    return await handle_error(request, err, err.message, status.HTTP_500_INTERNAL_SERVER_ERROR)


async def unknown_exception_handler(request: Request, err: Exception) -> ORJSONResponse:
    return await handle_error(request, err, "Internal server error", status.HTTP_500_INTERNAL_SERVER_ERROR)


async def handle_error(_: Request, err: Exception, message: str, status_code: int) -> ORJSONResponse:
    if isinstance(err, (ApplicationError, HTTPException)):
        logger.error("Handle error", extra={"error": err, "detail": message})
    else:
        logger.error("Handle unknown error", extra={"error": err}, exc_info=True)

    return ORJSONResponse(jsonable_encoder(ErrorResponse(message=message)), status_code=status_code)
