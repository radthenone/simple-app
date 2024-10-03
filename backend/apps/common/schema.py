import pydantic


class ErrorResponse(pydantic.BaseModel):
    detail: str


class SuccessResponse(pydantic.BaseModel):
    detail: str
