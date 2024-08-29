import enum

from pydantic import BaseModel
from typing import Optional


class ResponseModel(BaseModel):
    pass


class ResponseStatus(enum.Enum):
    SUCCESS = (200, "Success")
    CREATED = (201, "Created")
    BAD_REQUEST = (400, "Invalid request")
    NOT_FOUND = (404, "Resource not found")
    INTERNAL_ERROR = (500, "Internal server error")

    def __init__(self, status_code: int, status_msg: str):
        self.status_code = status_code
        self.status_msg = status_msg


class ResponseFailure:
    def __init__(self, status: ResponseStatus, details: Optional[str]):
        self.status_code = status.status_code
        self.err_msg = status.status_msg
        self.details = details


class ResponseSuccess:
    def __init__(self, data: ResponseModel, status: ResponseStatus):
        self.data = data
        self.status = status.status_code
