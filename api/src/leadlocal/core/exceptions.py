"""Application-level exceptions and FastAPI error handlers."""

from fastapi import HTTPException, status


class AppException(HTTPException):
    def __init__(self, detail: str, status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)


class NotFoundError(AppException):
    def __init__(self, resource: str = "Resource"):
        super().__init__(f"{resource} not found", status.HTTP_404_NOT_FOUND)


class AuthenticationError(AppException):
    def __init__(self, detail: str = "Invalid credentials"):
        super().__init__(detail, status.HTTP_401_UNAUTHORIZED)


class ForbiddenError(AppException):
    def __init__(self, detail: str = "Insufficient permissions"):
        super().__init__(detail, status.HTTP_403_FORBIDDEN)


class TierLimitError(AppException):
    def __init__(self, resource: str = "leads"):
        super().__init__(
            f"You have reached the {resource} limit for your plan. Please upgrade.",
            status.HTTP_402_PAYMENT_REQUIRED,
        )


class ConflictError(AppException):
    def __init__(self, detail: str = "Resource already exists"):
        super().__init__(detail, status.HTTP_409_CONFLICT)


class ExternalAPIError(AppException):
    def __init__(self, service: str, detail: str = ""):
        msg = f"{service} API error"
        if detail:
            msg += f": {detail}"
        super().__init__(msg, status.HTTP_502_BAD_GATEWAY)
