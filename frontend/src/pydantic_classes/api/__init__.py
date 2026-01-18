"""Pydantic models for reComm API."""

from .auth import *
from .friendship import *
from .group import *
from .message import *
from .base import *

__all__ = [
    # Base
    "BaseRequestAuthenticated",
    "BaseResponse",
    "EmptyBody",
    
    # Auth
    "AuthRequest",
    "AuthResponse",
    "RegisterRequest",
    "RegisterResponse",
    
    # Friendship
    "SendFriendRequestRequest",
    "SendFriendRequestResponse",
    "AcceptFriendRequestRequest",
    "AcceptFriendRequestResponse",
    "RejectFriendRequestRequest",
    "RejectFriendRequestResponse",
    "GetFriendsRequest",
    "GetFriendsResponse",
    "GetPendingRequestsRequest",
    "GetPendingRequestsResponse",
    "FriendshipRequest",
    
    # Group
    "CreateGroupRequest",
    "CreateGroupResponse",
    "AddMemberToGroupRequest",
    "AddMemberToGroupResponse",
    "UpdateGroupNameRequest",
    "UpdateGroupNameResponse",
    "LeaveGroupRequest",
    "LeaveGroupResponse",
    "DeleteGroupRequest",
    "DeleteGroupResponse",
    "GetUserGroupsResponse",
    "GetUserGroupsRequest",
    "GetGroupDetailsRequest",
    "GetGroupDetailsResponse",
    "GetGroupMembersRequest",
    "GetGroupMembersResponse",
    "Group",
    "GroupMember",

    # Message
    "MessageType",
    "MessageModel",
    "SendGroupMessageRequest",
    "SendGroupMessageResponse",
    "GetGroupMessagesRequest",
    "GetGroupMessagesResponse",
    "SendPrivateMessageRequest",
    "SendPrivateMessageResponse",
    "GetPrivateMessagesRequest",
    "GetPrivateMessagesResponse",
    "SendMessageRequest",
    "SendMessageResponse",
    "GetRecentMessagesRequest",
    "GetRecentMessagesResponse",
    
    # API methods
    "APIMethod",
]
