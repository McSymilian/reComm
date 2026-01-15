"""Authentication API models."""
from typing import Optional
from pydantic import BaseModel, Field
from .base import BaseRequest, BaseResponse
from .api_method import APIMethod


class AuthBody(BaseModel):
    """Payload for AUTH requests."""

    username: str = Field(..., description="Username for authentication")
    password: str = Field(..., description="Password for authentication")


class AuthRequest(BaseRequest):
    """Request model for user authentication (AUTH)."""

    method: APIMethod = Field(APIMethod.AUTH)
    body: AuthBody


class AuthResponse(BaseResponse):
    """Response model for successful authentication."""
    
    token: Optional[str] = Field(None, description="JWT token for authenticated sessions")


class RegisterBody(BaseModel):
    """Payload for REGISTER requests."""

    username: str = Field(..., description="Desired username")
    password: str = Field(..., description="Password for the new account")


class RegisterRequest(BaseRequest):
    """Request model for user registration (REGISTER)."""

    method: APIMethod = Field(APIMethod.REGISTER)
    body: RegisterBody

    
class RegisterResponse(BaseResponse):
    """Response model for successful registration."""
    
    token: Optional[str] = Field(None, description="JWT token for the newly registered user")
