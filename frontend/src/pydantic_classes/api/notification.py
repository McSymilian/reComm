from enum import Enum
from pydantic import BaseModel, Field, field_validator

class NotificationType(str, Enum):
    FRIEND_REQUEST = "FRIEND_REQUEST"
    NEW_PRIVATE_MESSAGE = "NEW_PRIVATE_MESSAGE"
    NEW_GROUP_MESSAGE = "NEW_GROUP_MESSAGE"



class BaseNotificationModel(BaseModel):
    type: NotificationType = Field(..., description="Type of notification", alias="type")
    sentAt: int = Field(..., description="Unix timestamp when the notification was sent", alias="sentAt")

    @field_validator('sentAt', mode='before')
    @classmethod
    def cast_sent_at_to_int(cls, v):
        """Auto-cast float timestamps to int."""
        if isinstance(v, float):
            return int(v)
        return v


class NewPrivateMessageNotificationModel(BaseNotificationModel):
    type: str = NotificationType.NEW_PRIVATE_MESSAGE
    messageId: str = Field(..., description="UUID of the new private message", alias="messageId")
    senderId: str = Field(..., description="UUID of the sender", alias="senderId")
    senderName: str = Field(..., description="Username of the sender", alias="senderName")
    content: str = Field(..., description="Content of the private message")


class NewGroupMessageNotificationModel(BaseNotificationModel):
    type: str = NotificationType.NEW_GROUP_MESSAGE
    messageId: str = Field(..., description="UUID of the new group message", alias="messageId")
    groupId: str = Field(..., description="UUID of the group", alias="groupId")
    senderId: str = Field(..., description="UUID of the sender", alias="senderId")
    senderName: str = Field(..., description="Username of the sender", alias="senderName")
    content: str = Field(..., description="Content of the group message")

class FriendRequestNotificationModel(BaseModel):
    type: str = NotificationType.FRIEND_REQUEST
    from_: str = Field(..., description="UUID of the friend request", alias="from")
    message: str = Field(..., description="UUID of the requester", alias="message")

