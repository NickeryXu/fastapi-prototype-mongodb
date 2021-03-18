from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from typing import Union
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.constants import REF_PREFIX
from fastapi.openapi.utils import validation_error_response_definition
from pydantic import ValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from loguru import logger
import traceback


async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    logger.error(exc.detail)
    return JSONResponse({"errors": [{'msg': exc.detail}]}, status_code=exc.status_code)


async def http422_error_handler(
        _: Request, exc: Union[RequestValidationError, ValidationError],
) -> JSONResponse:
    logger.error(exc.errors())
    return JSONResponse(
        {"errors": exc.errors()}, status_code=HTTP_422_UNPROCESSABLE_ENTITY,
    )


async def catch_exceptions_middleware(request: Request, call_next) -> JSONResponse:
    try:
        return await call_next(request)
    except Exception as e:
        traceback.print_exc()
        logger.error(e)
        # you probably want some kind of logging here
        return JSONResponse({"errors": [{'msg': "Internal server error"}]}, status_code=500)


validation_error_response_definition["properties"] = {
    "errors": {
        "title": "Errors",
        "type": "array",
        "items": {"$ref": "{0}ValidationError".format(REF_PREFIX)},
    },
}
