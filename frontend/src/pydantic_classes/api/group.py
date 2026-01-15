"""Group API models."""

from typing import List, Optional
from pydantic import BaseModel, Field, conlist
from .api_method import APIMethod
from .base import BaseRequestAuthenticated, BaseResponse, EmptyBody


class GroupMember(BaseModel):
    """Model for a group member."""
    
    uuid: str = Field(..., description="UUID of the member")
    username: str = Field(..., description="Username of the member")


class Group(BaseModel):
    """Model for a group."""
    
    groupId: str = Field(..., description="UUID of the group", alias="groupId")
    name: str = Field(..., description="Name of the group")
    creatorId: str = Field(..., description="UUID of the group creator", alias="creatorId")
    members: List[str] = Field(
        default_factory=list, 
        description="List of member UUIDs"
    )
    createdAt: int = Field(..., description="Creation timestamp", alias="createdAt")
    updatedAt: int = Field(..., description="Last update timestamp", alias="updatedAt")


class CreateGroupBody(BaseModel):
    groupName: str = Field(..., description="Name for the new group")


class CreateGroupRequest(BaseRequestAuthenticated):
    """Request model for creating a group (CREATE_GROUP)."""
    
    method: APIMethod = Field(APIMethod.CREATE_GROUP, )
    body: CreateGroupBody


class CreateGroupResponse(BaseResponse):
    """Response model for creating a group."""
    
    groupId: Optional[str] = Field(None, description="UUID of the created group", alias="groupId")


class AddMemberToGroupBody(BaseModel):
    groupId: str = Field(..., description="UUID of the group", alias="groupId")
    username: str = Field(..., description="Username to add to the group")


class AddMemberToGroupRequest(BaseRequestAuthenticated):
    """Request model for adding a member to a group (ADD_MEMBER_TO_GROUP)."""
    
    method: APIMethod = Field(APIMethod.ADD_MEMBER_TO_GROUP, )
    body: AddMemberToGroupBody


class AddMemberToGroupResponse(BaseResponse):
    """Response model for adding a member to a group."""
    pass


class UpdateGroupNameBody(BaseModel):
    groupId: str = Field(..., description="UUID of the group", alias="groupId")
    newName: str = Field(..., description="New name for the group", alias="newName")


class UpdateGroupNameRequest(BaseRequestAuthenticated):
    """Request model for updating a group name (UPDATE_GROUP_NAME)."""
    
    method: APIMethod = Field(APIMethod.UPDATE_GROUP_NAME, )
    body: UpdateGroupNameBody


class UpdateGroupNameResponse(BaseResponse):
    """Response model for updating a group name."""
    pass


class LeaveGroupBody(BaseModel):
    groupId: str = Field(..., description="UUID of the group to leave", alias="groupId")


class LeaveGroupRequest(BaseRequestAuthenticated):
    """Request model for leaving a group (LEAVE_GROUP)."""
    
    method: APIMethod = Field(APIMethod.LEAVE_GROUP)
    body: LeaveGroupBody


class LeaveGroupResponse(BaseResponse):
    """Response model for leaving a group."""
    pass


class DeleteGroupBody(BaseModel):
    groupId: str = Field(..., description="UUID of the group to delete", alias="groupId")


class DeleteGroupRequest(BaseRequestAuthenticated):
    """Request model for deleting a group (DELETE_GROUP)."""
    
    method: APIMethod = Field(APIMethod.DELETE_GROUP, )
    body: DeleteGroupBody


class DeleteGroupResponse(BaseResponse):
    """Response model for deleting a group."""
    pass


class GetUserGroupsRequest(BaseRequestAuthenticated):
    """Request model for getting user's groups (GET_USER_GROUPS)."""

    method: APIMethod = Field(APIMethod.GET_USER_GROUPS, )
    body: EmptyBody = Field(default=EmptyBody())


class GetUserGroupsResponse(BaseResponse):
    """Response model for getting user's groups (GET_USER_GROUPS)."""
    
    groups: List[Group] = Field([], description="List of user's groups")


class GetGroupDetailsBody(BaseModel):
    groupId: str = Field(..., description="UUID of the group", alias="groupId")


class GetGroupDetailsRequest(BaseRequestAuthenticated):
    """Request model for getting group details (GET_GROUP_DETAILS)."""
    
    method: APIMethod = Field(APIMethod.GET_GROUP_DETAILS, )
    body: GetGroupDetailsBody


class GetGroupDetailsResponse(BaseResponse):
    """Response model for getting group details."""
    
    group: Optional[Group] = Field(None, description="Group details")


class GetGroupMembersBody(BaseModel):
    groupId: str = Field(..., description="UUID of the group", alias="groupId")


class GetGroupMembersRequest(BaseRequestAuthenticated):
    """Request model for getting group members (GET_GROUP_MEMBERS)."""
    
    method: APIMethod = Field(APIMethod.GET_GROUP_MEMBERS, )
    body: GetGroupMembersBody


class GetGroupMembersResponse(BaseResponse):
    """Response model for getting group members."""
    
    members: List[GroupMember] = Field(
        default_factory=list,
        description="List of group members"
    )
