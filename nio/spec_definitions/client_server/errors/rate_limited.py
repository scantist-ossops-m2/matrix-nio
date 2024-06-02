# generated by datamodel-codegen:
#   filename:  rate_limited.yaml
#   timestamp: 2024-06-01T22:41:46+00:00

from __future__ import annotations

from typing import Optional

from aiohttp import ClientResponse
from pydantic import ConfigDict, Field

from .error import Error


class ErrorResponse(Error):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    errcode: str = Field(
        "unknown error",
        description="The M_LIMIT_EXCEEDED error code",
        examples=["M_LIMIT_EXCEEDED"],
    )
    error: Optional[str] = Field(
        None,
        description="A human-readable error message.",
        examples=["Too many requests"],
    )
    retry_after_ms: Optional[int] = Field(
        None,
        description="The amount of time in milliseconds the client should wait\nbefore trying the request again.",
        examples=[2000],
    )
    soft_logout: Optional[bool] = Field(
        default=None,
        description="If true within a 401 response, the client can offer to re-log in the user.",
    )

    transport_response: ClientResponse = Field(
        ...,
        description="The underlying transport response that contains the response body.",
    )

    @property
    def message(self) -> str:
        return self.error

    @property
    def status_code(self) -> str:
        return self.errcode

    def __str__(self) -> str:
        if self.status_code and self.message:
            error = f"{self.status_code} {self.message}"
        elif self.message:
            error = self.message
        elif self.status_code:
            error = f"{self.status_code} unknown error"
        else:
            error = "unknown error"

        if self.retry_after_ms:
            error = f"{error} - retry after {self.retry_after_ms}ms"

        return f"{self.__class__.__name__}: {error}"
