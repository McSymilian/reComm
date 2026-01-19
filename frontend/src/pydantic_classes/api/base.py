"""Base Pydantic models for API requests and responses."""

from typing import Optional
from .api_method import APIMethod
from pydantic import BaseModel, Field


class BaseRequest(BaseModel):
    """Base class for all API requests.

    Every request includes the backend method name and a body payload object.
    """

    method: APIMethod = Field(..., description="method for the request")
    body: object = Field(..., description="body of the request")

    class Config:
        from_attributes = True


class BaseRequestAuthenticated(BaseRequest):
    """Base class for all authenticated API requests.

    Every request includes the backend method name and a body payload object.
    """

    token: str = Field(..., description="JWT token for authentication")
    
    class Config:
        from_attributes = True



class BaseResponse(BaseModel):
    """Base class for all API responses."""
    
    code: int = Field(..., description="HTTP status code")
    message: Optional[str] = Field(None, description="Response message")
    
    class Config:
        from_attributes = True


class EmptyBody(BaseModel):
    """Empty request body for methods with no payload."""

    pass
