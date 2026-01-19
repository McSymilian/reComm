# reComm API Pydantic Models

This package contains Pydantic models for all API calls and responses in the reComm application.

## Features

- ✅ Full type validation for all API requests and responses
- ✅ Auto-completion support in IDEs
- ✅ Built-in serialization/deserialization
- ✅ Field validation and error handling
- ✅ Complete API client with type-safe methods

## Structure

```
pydantic_classes/
├── __init__.py         # Package exports
├── base.py            # Base models (BaseRequest, BaseResponse, ErrorResponse)
├── auth.py            # Authentication models (login, register)
├── friendship.py      # Friendship models (friend requests, friends list)
├── group.py           # Group models (create, manage groups)
├── message.py         # Messaging models (group/private messages)
├── api_client.py      # API client with all methods
└── examples.py        # Usage examples
```

## Installation

The required dependencies are already in `pyproject.toml`. Ensure `pydantic` is installed:

```bash
uv add pydantic
```

## Quick Start

### Using the API Client

```python
from pydantic_classes import APIClient

# Initialize the client
client = APIClient(host="localhost", port=8080)

# Register a new user
response = client.register(username="john_doe", password="secure123")
client.set_token(response.token)

# Send a friend request
client.send_friend_request(addressee_username="jane_doe")

# Create a group
group_response = client.create_group(group_name="Study Group")
print(f"Created group: {group_response.groupId}")
```

### Using Models Directly

```python
from pydantic_classes import AuthRequest, AuthResponse

# Validate request data
auth_req = AuthRequest(username="john_doe", password="secure123")

# Convert to dictionary
request_data = auth_req.model_dump()

# Parse response
response_data = {"code": 200, "message": "Success", "token": "jwt_token_here"}
auth_resp = AuthResponse(**response_data)
print(auth_resp.token)
```

## API Methods

### Authentication

- `authenticate(username, password)` → `AuthResponse`
- `register(username, password)` → `RegisterResponse`

### Friendship

- `send_friend_request(addressee_username)` → `SendFriendRequestResponse`
- `accept_friend_request(requester)` → `AcceptFriendRequestResponse`
- `reject_friend_request(requester)` → `RejectFriendRequestResponse`
- `get_friends()` → `GetFriendsResponse`
- `get_pending_requests()` → `GetPendingRequestsResponse`

### Groups

- `create_group(group_name)` → `CreateGroupResponse`
- `add_member_to_group(group_id, username)` → `AddMemberToGroupResponse`
- `update_group_name(group_id, new_name)` → `UpdateGroupNameResponse`
- `leave_group(group_id)` → `LeaveGroupResponse`
- `delete_group(group_id)` → `DeleteGroupResponse`
- `get_user_groups()` → `GetUserGroupsResponse`
- `get_group_details(group_id)` → `GetGroupDetailsResponse`
- `get_group_members(group_id)` → `GetGroupMembersResponse`

### Messages

- `send_group_message(group_id, content)` → `SendGroupMessageResponse`
- `get_group_messages(group_id, limit=100, offset=0, since=None)` → `GetGroupMessagesResponse`
- `send_private_message(receiver_username, content)` → `SendPrivateMessageResponse`
- `get_private_messages(other_username, limit=100, offset=0, since=None)` → `GetPrivateMessagesResponse`
- `send_message(group_id, content)` → `SendMessageResponse` (alias of group send)
- `get_recent_messages(group_id, limit=100)` → `GetRecentMessagesResponse`

## Models Overview

### Base Models

- **BaseRequest**: Base class for all requests
- **BaseResponse**: Base class for all responses (includes `code` and `message`)
- **ErrorResponse**: Error response with optional error details

### Authentication Models

- **AuthRequest** / **AuthResponse**: User login
- **RegisterRequest** / **RegisterResponse**: User registration

### Friendship Models

- **SendFriendRequestRequest** / **SendFriendRequestResponse**
- **AcceptFriendRequestRequest** / **AcceptFriendRequestResponse**
- **RejectFriendRequestRequest** / **RejectFriendRequestResponse**
- **GetFriendsResponse**: Returns list of friend usernames
- **GetPendingRequestsResponse**: Returns pending friend requests
- **FriendshipRequest**: Model for a single friendship request

### Group Models

- **Group**: Complete group information
- **GroupMember**: Group member with UUID and username
- **CreateGroupRequest** / **CreateGroupResponse**
- **AddMemberToGroupRequest** / **AddMemberToGroupResponse**
- **UpdateGroupNameRequest** / **UpdateGroupNameResponse**
- **LeaveGroupRequest** / **LeaveGroupResponse**
- **DeleteGroupRequest** / **DeleteGroupResponse**
- **GetUserGroupsResponse**: Returns list of user's groups
- **GetGroupDetailsRequest** / **GetGroupDetailsResponse**
- **GetGroupMembersRequest** / **GetGroupMembersResponse**

### Message Models

- **MessageModel**, **MessageType**
- **SendGroupMessageRequest** / **SendGroupMessageResponse**
- **GetGroupMessagesRequest** / **GetGroupMessagesResponse**
- **SendPrivateMessageRequest** / **SendPrivateMessageResponse**
- **GetPrivateMessagesRequest** / **GetPrivateMessagesResponse**
- **SendMessageRequest** / **SendMessageResponse** (alias)
- **GetRecentMessagesRequest** / **GetRecentMessagesResponse**

## Field Aliases

Some fields use camelCase in the backend but snake_case in Python. Pydantic handles this automatically:

```python
# Backend expects "addresseeUsername"
request = SendFriendRequestRequest(addresseeUsername="jane_doe")

# Serialize with aliases for backend
data = request.model_dump(by_alias=True)  # {"addresseeUsername": "jane_doe"}
```

## Validation

Pydantic automatically validates all data:

```python
from pydantic import ValidationError
from pydantic_classes import AuthRequest

try:
    # This will raise ValidationError - username is required
    auth = AuthRequest(password="only_password")
except ValidationError as e:
    print(e)
```

## Error Handling

```python
from pydantic_classes import APIClient, ErrorResponse

client = APIClient()

try:
    response = client.authenticate(username="user", password="pass")
    print(f"Success: {response.token}")
except ValidationError as e:
    print(f"Validation error: {e}")
except Exception as e:
    print(f"API error: {e}")
```

## Integration with UI

Example integration with the login frame:

```python
from pydantic_classes import APIClient

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, on_login_success, **kwargs):
        super().__init__(master, **kwargs)
        self.api_client = APIClient(host="localhost", port=8080)
        # ... rest of init
    
    def handle_login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        try:
            response = self.api_client.authenticate(username, password)
            self.api_client.set_token(response.token)
            self.error_label.configure(text="")
            self.on_login_success(username, response.token)
        except Exception as e:
            self.error_label.configure(text=f"Login failed: {e}")
```

## TODO

- [ ] Implement actual socket/websocket communication in `APIClient._send_request()`
- [ ] Add async support for API calls
- [ ] Add retry logic and error handling
- [x] Add message/chat-related models
- [ ] Add notification models

## Notes

The `APIClient._send_request()` method is currently a placeholder. You need to implement the actual socket or WebSocket communication based on your backend protocol.



<!--  klasy pydantic wygenerowane z pomocą sztucznej inteligencji na podstawie dokumentacji API - dla wygody programowania -->