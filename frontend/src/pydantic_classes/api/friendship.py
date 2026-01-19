"""Friendship API models."""

from typing import List
from pydantic import BaseModel, Field
from .api_method import APIMethod
from .base import BaseRequestAuthenticated, BaseResponse, EmptyBody


class SendFriendRequestBody(BaseModel):
    """Payload for sending a friend request."""

    addresseeUsername: str = Field(
        ..., description="Username of the person to send friend request to"
    )


class SendFriendRequestRequest(BaseRequestAuthenticated):
    """Request model for sending a friend request (SEND_FRIEND_REQUEST)."""

    method: APIMethod = Field(APIMethod.SEND_FRIEND_REQUEST, )
    body: SendFriendRequestBody


class SendFriendRequestResponse(BaseResponse):
    """Response model for sending a friend request."""
    pass


class AcceptFriendRequestBody(BaseModel):
    """Payload for accepting a friend request."""

    requester: str = Field(..., description="Username of the person who sent the friend request")


class AcceptFriendRequestRequest(BaseRequestAuthenticated):
    """Request model for accepting a friend request (ACCEPT_FRIEND_REQUEST)."""

    method: APIMethod = Field(APIMethod.ACCEPT_FRIEND_REQUEST, )
    body: AcceptFriendRequestBody


class AcceptFriendRequestResponse(BaseResponse):
    """Response model for accepting a friend request."""
    pass


class RejectFriendRequestBody(BaseModel):
    """Payload for rejecting a friend request."""

    requester: str = Field(..., description="Username of the person who sent the friend request")


class RejectFriendRequestRequest(BaseRequestAuthenticated):
    """Request model for rejecting a friend request (REJECT_FRIEND_REQUEST)."""

    method: APIMethod = Field(APIMethod.REJECT_FRIEND_REQUEST, )
    body: RejectFriendRequestBody


class RejectFriendRequestResponse(BaseResponse):
    """Response model for rejecting a friend request."""
    pass


class GetFriendsRequest(BaseRequestAuthenticated):
    """Request model for getting friends list (GET_FRIENDS)."""

    method: APIMethod = Field(APIMethod.GET_FRIENDS)
    body: EmptyBody = Field(default=EmptyBody())


# class FriendModel(BaseModel):
#     """Model for a friend."""

#     username: str = Field(..., description="Username of the friend")
#     uuid: str = Field(..., description="UUID of the friend")

class GetFriendsResponse(BaseResponse):
    """Response model for getting friends list (GET_FRIENDS)."""
    
    friends: List[str] = Field(
        default_factory=list, 
        description="List of friends"
    )


class FriendshipRequest(BaseModel):
    """Model for a pending friendship request."""
    
    requester: str = Field(..., description="Username who sent the request")
    addressee: str = Field(..., description="Username who received the request")
    status: int = Field(..., description="Status of the friendship request")


class GetPendingRequestsRequest(BaseRequestAuthenticated):
    """Request model for getting pending friend requests (GET_PENDING_REQUESTS)."""

    method: APIMethod = Field(APIMethod.GET_PENDING_REQUESTS, )
    body: EmptyBody = Field(default=EmptyBody())


class GetPendingRequestsResponse(BaseResponse):
    """Response model for getting pending friend requests (GET_PENDING_REQUESTS)."""
    
    pendingRequests: List[FriendshipRequest] = Field(
        default_factory=list,
        description="List of pending friendship requests",
        alias="pendingRequests"
    )
