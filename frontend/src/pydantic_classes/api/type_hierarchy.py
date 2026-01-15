"""
Type hierarchy and relationships for reComm Pydantic models.

This file provides a visual overview of all models and their inheritance.
Not meant to be executed - for documentation purposes only.
"""

# BASE HIERARCHY
# ==============

class BaseRequest:
    """Base for all API requests"""
    pass

class BaseResponse:
    """
    Base for all API responses
    
    Fields:
        - code: int
        - message: str
    """
    pass

class ErrorResponse(BaseResponse):
    """
    Error response
    
    Additional Fields:
        - error: Optional[str]
    """
    pass


# AUTHENTICATION MODELS
# =====================

class AuthRequest(BaseRequest):
    """Fields: username, password"""
    pass

class AuthResponse(BaseResponse):
    """Fields: code, message, token"""
    pass

class RegisterRequest(BaseRequest):
    """Fields: username, password"""
    pass

class RegisterResponse(BaseResponse):
    """Fields: code, message, token"""
    pass


# FRIENDSHIP MODELS
# =================

class SendFriendRequestRequest(BaseRequest):
    """Fields: addresseeUsername"""
    pass

class SendFriendRequestResponse(BaseResponse):
    """Fields: code, message"""
    pass

class AcceptFriendRequestRequest(BaseRequest):
    """Fields: requester"""
    pass

class AcceptFriendRequestResponse(BaseResponse):
    """Fields: code, message"""
    pass

class RejectFriendRequestRequest(BaseRequest):
    """Fields: requester"""
    pass

class RejectFriendRequestResponse(BaseResponse):
    """Fields: code, message"""
    pass

class GetFriendsResponse(BaseResponse):
    """Fields: code, message, friends: List[str]"""
    pass

class FriendshipRequest(BaseRequest):
    """Fields: requester, addressee, status"""
    pass

class GetPendingRequestsResponse(BaseResponse):
    """Fields: code, message, pendingRequests: List[FriendshipRequest]"""
    pass


# GROUP MODELS
# ============

class GroupMember(BaseRequest):
    """Fields: uuid, username"""
    pass

class Group(BaseRequest):
    """
    Fields:
        - groupId: str
        - name: str
        - creatorId: str
        - members: List[str]
        - createdAt: int
        - updatedAt: int
    """
    pass

class CreateGroupRequest(BaseRequest):
    """Fields: groupName"""
    pass

class CreateGroupResponse(BaseResponse):
    """Fields: code, message, groupId"""
    pass

class AddMemberToGroupRequest(BaseRequest):
    """Fields: groupId, username"""
    pass

class AddMemberToGroupResponse(BaseResponse):
    """Fields: code, message"""
    pass

class UpdateGroupNameRequest(BaseRequest):
    """Fields: groupId, newName"""
    pass

class UpdateGroupNameResponse(BaseResponse):
    """Fields: code, message"""
    pass

class LeaveGroupRequest(BaseRequest):
    """Fields: groupId"""
    pass

class LeaveGroupResponse(BaseResponse):
    """Fields: code, message"""
    pass

class DeleteGroupRequest(BaseRequest):
    """Fields: groupId"""
    pass

class DeleteGroupResponse(BaseResponse):
    """Fields: code, message"""
    pass

class GetUserGroupsResponse(BaseResponse):
    """Fields: code, message, groups: List[Group]"""
    pass

class GetGroupDetailsRequest(BaseRequest):
    """Fields: groupId"""
    pass

class GetGroupDetailsResponse(BaseResponse):
    """Fields: code, message, group: Optional[Group]"""
    pass

class GetGroupMembersRequest(BaseRequest):
    """Fields: groupId"""
    pass

class GetGroupMembersResponse(BaseResponse):
    """Fields: code, message, members: List[GroupMember]"""
    pass


# API CLIENT
# ==========

class APIMethod:
    """
    Enum of all API methods:
    
    Authentication:
        - AUTH
        - REGISTER
    
    Friendship:
        - SEND_FRIEND_REQUEST
        - ACCEPT_FRIEND_REQUEST
        - REJECT_FRIEND_REQUEST
        - GET_FRIENDS
        - GET_PENDING_REQUESTS
    
    Groups:
        - CREATE_GROUP
        - ADD_MEMBER_TO_GROUP
        - UPDATE_GROUP_NAME
        - LEAVE_GROUP
        - DELETE_GROUP
        - GET_USER_GROUPS
        - GET_GROUP_DETAILS
        - GET_GROUP_MEMBERS
    """
    pass

class APIClient:
    """
    Type-safe API client with methods for all endpoints.
    
    Initialize:
        client = APIClient(host="localhost", port=8080)
    
    Authentication:
        - authenticate(username, password) -> AuthResponse
        - register(username, password) -> RegisterResponse
        - set_token(token)
        - clear_token()
    
    Friendship:
        - send_friend_request(addressee_username) -> SendFriendRequestResponse
        - accept_friend_request(requester) -> AcceptFriendRequestResponse
        - reject_friend_request(requester) -> RejectFriendRequestResponse
        - get_friends() -> GetFriendsResponse
        - get_pending_requests() -> GetPendingRequestsResponse
    
    Groups:
        - create_group(group_name) -> CreateGroupResponse
        - add_member_to_group(group_id, username) -> AddMemberToGroupResponse
        - update_group_name(group_id, new_name) -> UpdateGroupNameResponse
        - leave_group(group_id) -> LeaveGroupResponse
        - delete_group(group_id) -> DeleteGroupResponse
        - get_user_groups() -> GetUserGroupsResponse
        - get_group_details(group_id) -> GetGroupDetailsResponse
        - get_group_members(group_id) -> GetGroupMembersResponse
    """
    pass


# IMPORT STRUCTURE
# ================

"""
from pydantic_classes import (
    # API Client
    APIClient, APIMethod,
    
    # Base
    BaseRequest, BaseResponse, ErrorResponse,
    
    # Auth
    AuthRequest, AuthResponse,
    RegisterRequest, RegisterResponse,
    
    # Friendship
    SendFriendRequestRequest, SendFriendRequestResponse,
    AcceptFriendRequestRequest, AcceptFriendRequestResponse,
    RejectFriendRequestRequest, RejectFriendRequestResponse,
    GetFriendsResponse, GetPendingRequestsResponse,
    FriendshipRequest,
    
    # Groups
    CreateGroupRequest, CreateGroupResponse,
    AddMemberToGroupRequest, AddMemberToGroupResponse,
    UpdateGroupNameRequest, UpdateGroupNameResponse,
    LeaveGroupRequest, LeaveGroupResponse,
    DeleteGroupRequest, DeleteGroupResponse,
    GetUserGroupsResponse,
    GetGroupDetailsRequest, GetGroupDetailsResponse,
    GetGroupMembersRequest, GetGroupMembersResponse,
    Group, GroupMember,
)
"""
