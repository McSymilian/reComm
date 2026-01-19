from pydantic import BaseModel, Field
from pydantic_classes.api.message import MessageModel
from typing import List

class PrivateConversationDataModel(BaseModel):
    friendId: str = Field(..., description="UUID of the friend", alias="friendId")
    lastMessageAt: int = Field(..., description="Unix timestamp of the last message in the conversation", alias="lastMessageAt")
    friendName: str = Field(..., description="Username of the friend", alias="friendName")
    messages: List[MessageModel] = Field(..., description="List of messages in the conversation", alias="messages")