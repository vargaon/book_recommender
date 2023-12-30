from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field


class HTTPExceptionSchema(BaseModel):
    """Class to represent HTTP exception schema"""

    detail: Annotated[
        str,
        Field(..., title="Detail of exception", description="Text description of http exception"),
    ]


class HTTPBadRequestExceptionSchema(HTTPExceptionSchema):
    """Class to represent HTTP bad request exception schema"""

    name: Annotated[
        str, Field(..., title="Name", description="Name of bad parameter from request")
    ]
    value: Annotated[
        str, Field(..., title="Value", description="Value of bad parameter from request")
    ]

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "name": "Parameter name",
                "value": "Parameters value",
                "detail": "Detail of http exception",
            }
        },
    )


class HTTPNotFoundExceptionSchema(HTTPExceptionSchema):
    """Class to represent HTTP bad request exception schema"""

    model_config = ConfigDict(
        extra="forbid", json_schema_extra={"example": {"detail": "Detail of http exception"}}
    )


class HTTPMethodNotAllowedExceptionSchema(HTTPExceptionSchema):
    """Class to represent HTTP method not allowed exception schema"""

    model_config = ConfigDict(
        extra="forbid", json_schema_extra={"example": {"detail": "Detail of http exception"}}
    )


class HTTPUnauthorizedExceptionSchema(HTTPExceptionSchema):
    """Class to represent HTTP unauthorized exception schema"""

    model_config = ConfigDict(
        extra="forbid", json_schema_extra={"example": {"detail": "Detail of http exception"}}
    )


class HTTPServiceUnavailableExceptionSchema(HTTPExceptionSchema):
    """Class to represent HTTP service unavailable exception schema"""

    model_config = ConfigDict(
        extra="forbid", json_schema_extra={"example": {"detail": "Detail of http exception"}}
    )


class HTTPConflictExceptionSchema(HTTPExceptionSchema):
    """Class to represent HTTP conflict exception schema"""

    model_config = ConfigDict(
        extra="forbid", json_schema_extra={"example": {"detail": "Detail of http exception"}}
    )
