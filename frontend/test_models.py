#!/usr/bin/env python3
"""
Validation script to test all Pydantic models.
Run this to verify all models are correctly defined.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))


def test_base_models():
    """Test base models."""
    from pydantic_classes.base import BaseResponse, ErrorResponse
    
    # Test BaseResponse
    response = BaseResponse(code=200, message="Success")
    assert response.code == 200
    assert response.message == "Success"
    
    # Test ErrorResponse
    error = ErrorResponse(code=400, message="Bad Request", error="Invalid field")
    assert error.code == 400
    assert error.error == "Invalid field"
    
    print("✓ Base models OK")


def test_auth_models():
    """Test authentication models."""
    from pydantic_classes.auth import (
        AuthRequest, AuthResponse, RegisterRequest, RegisterResponse
    )
    
    # Test AuthRequest
    auth_req = AuthRequest(body={"username": "testuser", "password": "testpass"})
    assert auth_req.body.username == "testuser"
    assert auth_req.method.value == "AUTH"
    
    # Test AuthResponse
    auth_resp = AuthResponse(code=200, message="Authenticated", token="jwt_token")
    assert auth_resp.token == "jwt_token"
    
    # Test RegisterRequest
    reg_req = RegisterRequest(body={"username": "newuser", "password": "newpass"})
    assert reg_req.body.username == "newuser"
    assert reg_req.method.value == "REGISTER"
    
    # Test RegisterResponse
    reg_resp = RegisterResponse(code=201, message="Registered", token="new_token")
    assert reg_resp.token == "new_token"
    
    print("✓ Auth models OK")


def test_friendship_models():
    """Test friendship models."""
    from pydantic_classes.friendship import (
        SendFriendRequestRequest, AcceptFriendRequestRequest, RejectFriendRequestRequest,
        GetFriendsRequest, GetFriendsResponse,
        GetPendingRequestsRequest, GetPendingRequestsResponse, FriendshipRequest
    )
    
    # Test SendFriendRequestRequest
    send_req = SendFriendRequestRequest(body={"addresseeUsername": "friend1"})
    assert send_req.body.addresseeUsername == "friend1"
    
    # Test AcceptFriendRequestRequest
    accept_req = AcceptFriendRequestRequest(body={"requester": "friend2"})
    assert accept_req.body.requester == "friend2"

    # Test RejectFriendRequestRequest
    reject_req = RejectFriendRequestRequest(body={"requester": "friend3"})
    assert reject_req.body.requester == "friend3"

    # Empty-body requests
    gf_req = GetFriendsRequest()
    assert gf_req.method.value == "GET_FRIENDS"
    gpr_req = GetPendingRequestsRequest()
    assert gpr_req.method.value == "GET_PENDING_REQUESTS"
    
    # Test GetFriendsResponse
    friends_resp = GetFriendsResponse(
        code=200, 
        message="OK", 
        friends=["friend1", "friend2"]
    )
    assert len(friends_resp.friends) == 2
    
    # Test FriendshipRequest
    fr = FriendshipRequest(
        requester="user1",
        addressee="user2",
        status="pending"
    )
    assert fr.status == "pending"
    
    # Test GetPendingRequestsResponse
    pending_resp = GetPendingRequestsResponse(
        code=200,
        message="OK",
        pendingRequests=[fr]
    )
    assert len(pending_resp.pendingRequests) == 1
    
    print("✓ Friendship models OK")


def test_group_models():
    """Test group models."""
    from pydantic_classes.group import (
        CreateGroupRequest, CreateGroupResponse,
        Group, GroupMember, GetUserGroupsResponse, GetUserGroupsRequest,
        AddMemberToGroupRequest, GetGroupMembersResponse, GetGroupMembersRequest
    )
    
    # Test CreateGroupRequest
    create_req = CreateGroupRequest(body={"groupName": "Study Group"})
    assert create_req.body.groupName == "Study Group"
    
    # Test CreateGroupResponse
    create_resp = CreateGroupResponse(
        code=200,
        message="Created",
        groupId="group-uuid-123"
    )
    assert create_resp.groupId == "group-uuid-123"
    
    # Test GroupMember
    member = GroupMember(uuid="user-uuid", username="john")
    assert member.username == "john"
    
    # Test Group
    group = Group(
        groupId="group-123",
        name="Test Group",
        creatorId="creator-123",
        members=["user1", "user2"],
        createdAt=1234567890,
        updatedAt=1234567890
    )
    assert len(group.members) == 2
    
    # Test GetUserGroupsResponse
    groups_resp = GetUserGroupsResponse(
        code=200,
        message="OK",
        groups=[group]
    )
    assert len(groups_resp.groups) == 1
    
    # Test AddMemberToGroupRequest
    add_req = AddMemberToGroupRequest(body={"groupId": "group-123", "username": "newuser"})
    assert add_req.body.username == "newuser"

    get_members_req = GetGroupMembersRequest(body={"groupId": "group-123"})
    assert get_members_req.body.groupId == "group-123"

    get_user_groups_req = GetUserGroupsRequest()
    assert get_user_groups_req.method.value == "GET_USER_GROUPS"
    
    # Test GetGroupMembersResponse
    members_resp = GetGroupMembersResponse(
        code=200,
        message="OK",
        members=[member]
    )
    assert len(members_resp.members) == 1
    
    print("✓ Group models OK")


def test_message_models():
    """Test message models."""
    from pydantic_classes.message import (
        MessageModel, MessageType,
        SendGroupMessageRequest, SendGroupMessageResponse,
        GetGroupMessagesRequest, GetGroupMessagesResponse,
        SendPrivateMessageRequest, GetPrivateMessagesRequest,
        SendMessageRequest, GetRecentMessagesRequest,
    )

    # Test message model
    msg = MessageModel(
        messageId="msg-1",
        senderId="user-a",
        receiverId="group-1",
        type=MessageType.GROUP,
        content="hello",
        sentAt=1,
        deliveredAt=2,
    )
    assert msg.type == MessageType.GROUP

    # Test send group message request/response
    send_req = SendGroupMessageRequest(body={"groupId": "group-1", "content": "Hi"})
    assert send_req.body.groupId == "group-1"
    send_resp = SendGroupMessageResponse(code=200, message="ok", messageId="mid-1")
    assert send_resp.messageId == "mid-1"

    # Test get group messages request/response
    get_req = GetGroupMessagesRequest(body={"groupId": "group-1", "limit": 10, "offset": 0, "since": None})
    assert get_req.body.limit == 10
    get_resp = GetGroupMessagesResponse(code=200, message="ok", messages=[msg], count=1)
    assert get_resp.count == 1

    # Test private message requests
    private_req = SendPrivateMessageRequest(body={"receiverUsername": "bob", "content": "hey"})
    assert private_req.body.receiverUsername == "bob"
    history_req = GetPrivateMessagesRequest(body={"otherUsername": "bob", "limit": 5, "offset": 0, "since": None})
    assert history_req.body.otherUsername == "bob"

    # Test generic send + recent
    send_generic = SendMessageRequest(body={"groupId": "group-1", "content": "alias"})
    assert send_generic.body.content == "alias"
    recent_req = GetRecentMessagesRequest(body={"groupId": "group-1", "limit": 5})
    assert recent_req.body.limit == 5

    print("✓ Message models OK")


def test_api_client():
    """Test API client structure."""
    from pydantic_classes.api_client import APIClient, APIMethod
    from pydantic_classes.auth import AuthRequest
    
    # Test APIMethod enum
    assert APIMethod.AUTH == "AUTH"
    assert APIMethod.CREATE_GROUP == "CREATE_GROUP"
    assert APIMethod.SEND_FRIEND_REQUEST == "SEND_FRIEND_REQUEST"
    assert APIMethod.SEND_GROUP_MESSAGE == "SEND_GROUP_MESSAGE"
    
    # Test APIClient initialization
    client = APIClient(host="192.168.1.230", port=8080)
    assert client.host == "192.168.1.230"
    assert client.port == 8080
    assert client.token is None
    
    # Test token management
    client.set_token("test_token")
    assert client.token == "test_token"
    
    client.clear_token()
    assert client.token is None
    
    # Test _build_request
    request = client._build_request(AuthRequest, username="test", password="pass")
    assert request.method.value == "AUTH"
    assert request.body.username == "test"
    
    print("✓ API client OK")


def test_serialization():
    """Test model serialization."""
    from pydantic_classes import AuthRequest, CreateGroupRequest
    
    # Test basic serialization
    auth = AuthRequest(body={"username": "john", "password": "pass123"})
    data = auth.model_dump()
    assert data["body"] == {"username": "john", "password": "pass123"}
    assert data["method"] == "AUTH"
    
    # Test alias serialization
    group = CreateGroupRequest(body={"groupName": "My Group"})
    data_with_alias = group.model_dump(by_alias=True)
    assert data_with_alias["body"]["groupName"] == "My Group"
    
    print("✓ Serialization OK")


def test_validation():
    """Test Pydantic validation."""
    from pydantic import ValidationError
    from pydantic_classes import AuthRequest
    
    # Test required field validation
    try:
        AuthRequest(body={"username": "only_username"})  # Missing password
        assert False, "Should have raised ValidationError"
    except ValidationError:
        pass  # Expected
    
    print("✓ Validation OK")


def main():
    """Run all tests."""
    print("Testing reComm Pydantic models...\n")
    
    tests = [
        test_base_models,
        test_auth_models,
        test_friendship_models,
        test_group_models,
        test_message_models,
        test_api_client,
        test_serialization,
        test_validation,
    ]
    
    failed = []
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"✗ {test.__name__} FAILED: {e}")
            failed.append(test.__name__)
    
    print("\n" + "=" * 50)
    if not failed:
        print("✓ All tests passed!")
        print(f"Total: {len(tests)} tests")
        return 0
    else:
        print(f"✗ {len(failed)} test(s) failed:")
        for name in failed:
            print(f"  - {name}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
