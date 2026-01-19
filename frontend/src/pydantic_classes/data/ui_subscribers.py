from pydantic import Enum

class UISubscriberTypes(Enum):
    PRIVATE_CONVERSATIONS = "private_conversations"
    GROUP_CONVERSATIONS = "group_conversations"
    FRIEND_REQUESTS = "friend_requests"
    

