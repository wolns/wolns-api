import traceback
from typing import Any

from litestar import Request, Response


class AppError(Exception):
    status_code: int = 500
    error_code: str = "GENERIC_APPLICATION_ERROR"

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or self.error_code)
        self.message = message


class NotFoundException(AppError):
    status_code = 404
    error_code = "NOT_FOUND"


class AlreadyExistsError(AppError):
    status_code = 409
    error_code = "ALREADY_EXISTS"


class NotAuthorizedException(AppError):
    status_code = 401
    error_code = "NOT_AUTHORIZED"


class InvalidPartiesException(AppError):
    status_code = 400
    error_code = "INVALID_PARTIES"


class ValidationException(AppError):
    status_code = 400
    error_code = "VALIDATION_ERROR"


class ForbiddenException(AppError):
    status_code = 403
    error_code = "FORBIDDEN"


def app_error_handler(request: Request, exc: AppError) -> Response[dict[str, Any]]:
    return Response(
        status_code=exc.status_code,
        content={
            "detail": exc.message or str(exc),
            "code": exc.error_code,
        },
        media_type="application/json",
    )


def generic_handler(request: Request, exc: Exception) -> Response[dict[str, Any]]:
    print("\n--- UNHANDLED EXCEPTION IN APP ---")
    print(f"Request Path: {request.url.path}")
    print(f"Exception Type: {type(exc).__name__}")
    print(f"Exception Message: {exc}")
    print("Traceback:")
    traceback.print_exc()
    print("--- END UNHANDLED EXCEPTION ---\n")
    return Response(
        content={
            "detail": "An internal server error occurred.",
        },
        status_code=500,
    )
