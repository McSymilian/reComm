"""Messaging API models."""

from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field, field_validator
from .api_method import APIMethod

from .base import BaseRequestAuthenticated, BaseResponse


class MessageType(str, Enum):
    """Type of message."""
    PRIVATE = "PRIVATE"
    GROUP = "GROUP"


class MessageModel(BaseModel):
    """Represents a message entity returned by the backend."""

    messageId: str = Field(..., description="UUID of the message", alias="messageId")
    senderId: Optional[str] = Field(None, description="UUID of the sender", alias="senderId")
    receiverId: Optional[str] = Field(None, description="UUID of the receiver (user or group)", alias="receiverId")
    type: MessageType = Field(..., description="Message type: GROUP or PRIVATE")
    senderName: str = Field(..., description="Username of the sender", alias="senderName")
    content: str = Field(..., description="Message body")
    sentAt: int = Field(..., description="Unix timestamp when sent", alias="sentAt")
    deliveredAt: Optional[int] = Field(None, description="Unix timestamp when delivered", alias="deliveredAt")

    @field_validator('sentAt', 'deliveredAt', mode='before')
    @classmethod
    def cast_timestamps_to_int(cls, v):
        """Auto-cast float timestamps to int."""
        if isinstance(v, float):
            return int(v)
        return v

class SendGroupMessageBody(BaseModel):
    groupId: str = Field(..., description="UUID of the group", alias="groupId")
    content: str = Field(..., description="Message content")


class SendGroupMessageRequest(BaseRequestAuthenticated):
    """Request model for sending a group message (SEND_GROUP_MESSAGE)."""

    method: APIMethod = Field(APIMethod.SEND_GROUP_MESSAGE, )
    body: SendGroupMessageBody


class SendGroupMessageResponse(BaseResponse):
    """Response model for sending a group message."""

    messageId: Optional[str] = Field(None, description="UUID of the sent message", alias="messageId")


class GetGroupMessagesBody(BaseModel):
    groupId: str = Field(..., description="UUID of the group", alias="groupId")
    limit: int = Field(100, description="Maximum number of messages to fetch")
    offset: int = Field(0, description="Pagination offset")
    since: Optional[int] = Field(None, description="Unix timestamp to fetch messages since")


class GetGroupMessagesRequest(BaseRequestAuthenticated):
    """Request model for fetching group messages (GET_GROUP_MESSAGES)."""

    method: APIMethod = Field(APIMethod.GET_GROUP_MESSAGES, )
    body: GetGroupMessagesBody


class GetGroupMessagesResponse(BaseResponse):
    """Response model for fetching group messages."""

    messages: List[MessageModel] = Field(default_factory=list, description="List of messages")
    count: Optional[int] = Field(None, description="Number of messages returned")


class SendPrivateMessageBody(BaseModel):
    receiverUsername: str = Field(..., description="Username of the receiver", alias="receiverUsername")
    content: str = Field(..., description="Message content")


class SendPrivateMessageRequest(BaseRequestAuthenticated):
    """Request model for sending a private message (SEND_PRIVATE_MESSAGE)."""

    method: APIMethod = Field(APIMethod.SEND_PRIVATE_MESSAGE, )
    body: SendPrivateMessageBody


class SendPrivateMessageResponse(BaseResponse):
    """Response model for sending a private message."""

    messageId: Optional[str] = Field(None, description="UUID of the sent message", alias="messageId")


class GetPrivateMessagesBody(BaseModel):
    otherUsername: str = Field(..., description="Username of the other participant", alias="otherUsername")
    limit: int = Field(100, description="Maximum number of messages to fetch")
    offset: int = Field(0, description="Pagination offset")
    since: Optional[int] = Field(None, description="Unix timestamp to fetch messages since")


class GetPrivateMessagesRequest(BaseRequestAuthenticated):
    """Request model for fetching private messages (GET_PRIVATE_MESSAGES)."""

    method: APIMethod = Field(APIMethod.GET_PRIVATE_MESSAGES, )
    body: GetPrivateMessagesBody


class GetPrivateMessagesResponse(BaseResponse):
    """Response model for fetching private messages."""
    # can be empty if no messages exist between users
    messages: List[MessageModel] = Field(None, description="List of messages")
    count: Optional[int] = Field(None, description="Number of messages returned")




class SendMessageBody(BaseModel):
    groupId: str = Field(..., description="UUID of the group", alias="groupId")
    content: str = Field(..., description="Message content")


class SendMessageRequest(BaseRequestAuthenticated):
    """Request model for sending a message via SEND_MESSAGE (alias of group send)."""

    method: APIMethod = Field(APIMethod.SEND_MESSAGE, )
    body: SendMessageBody


class SendMessageResponse(BaseResponse):
    """Response model for SEND_MESSAGE."""

    messageId: Optional[str] = Field(None, description="UUID of the sent message", alias="messageId")


class GetRecentMessagesBody(BaseModel):
    groupId: str = Field(..., description="UUID of the group", alias="groupId")
    limit: int = Field(100, description="Maximum number of messages to fetch")


class GetRecentMessagesRequest(BaseRequestAuthenticated):
    """Request model for fetching recent messages (GET_RECENT_MESSAGES)."""

    method: APIMethod = Field(APIMethod.GET_RECENT_MESSAGES, )
    body: GetRecentMessagesBody


class GetRecentMessagesResponse(BaseResponse):
    """Response model for fetching recent messages."""

    messages: List[MessageModel] = Field(default_factory=list, description="List of messages")
    count: Optional[int] = Field(None, description="Number of messages returned")
