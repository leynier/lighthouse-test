from fastapi import HTTPException, status
from pydantic import BaseModel


class DetailSchema(BaseModel):
    status_code: int
    detail: str


class BadRequest(HTTPException):
    def __init__(self, message: str | None = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message if message else "Bad Request",
        )


class Conflict(HTTPException):
    def __init__(self, message: str | None = None):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=message if message else "Conflict",
        )


class Forbidden(HTTPException):
    def __init__(self, message: str | None = None):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message if message else "Forbidden",
        )


class NotFound(HTTPException):
    def __init__(self, object_name: str | None = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{object_name if object_name else 'Entity'} not found",
        )


class ServerError(HTTPException):
    def __init__(self, message: str | None = None):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=message if message else "Internal Server Error",
        )


bad_request_response = {
    "description": "Bad Request Error",
    "model": DetailSchema,
}

conflict_response = {
    "description": "Conflict Error",
    "model": DetailSchema,
}

forbidden_response = {
    "description": "Forbidden Error",
    "model": DetailSchema,
}

not_found_response = {
    "description": "Not Found Error",
    "model": DetailSchema,
}

server_error_response = {
    "description": "Server Error",
    "model": DetailSchema,
}
