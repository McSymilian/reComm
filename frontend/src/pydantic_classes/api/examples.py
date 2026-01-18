"""Example usage of reComm API Pydantic models and client."""

from frontend.src.pydantic_classes.api import (
    APIClient,
    AuthRequest,
    RegisterRequest,
    CreateGroupRequest,
    SendFriendRequestRequest,
)


def example_authentication():
    """Example: Authenticate and register users."""
    
    # Create API client
    client = APIClient(host="192.168.100.44", port=8080)
    
    # Register a new user
    try:
        response = client.register(username="john_doe", password="secure123")
        print(f"Registration successful! Token: {response.token}")
        client.set_token(response.token)
    except Exception as e:
        print(f"Registration failed: {e}")
    
    # Authenticate existing user
    try:
        response = client.authenticate(username="john_doe", password="secure123")
        print(f"Authentication successful! Token: {response.token}")
        client.set_token(response.token)
    except Exception as e:
        print(f"Authentication failed: {e}")


def example_friendship_operations():
    """Example: Friendship operations."""
    
    client = APIClient(host="192.168.100.44", port=8080)
    # Assume we're already authenticated
    client.set_token("your_jwt_token_here")
    
    # Send a friend request
    try:
        response = client.send_friend_request(addressee_username="jane_doe")
        print(f"Friend request sent: {response.message}")
    except Exception as e:
        print(f"Failed to send friend request: {e}")
    
    # Get pending friend requests
    try:
        response = client.get_pending_requests()
        print(f"Pending requests: {len(response.pendingRequests)}")
        for req in response.pendingRequests:
            print(f"  - From: {req.requester}, Status: {req.status}")
    except Exception as e:
        print(f"Failed to get pending requests: {e}")
    
    # Accept a friend request
    try:
        response = client.accept_friend_request(requester="jane_doe")
        print(f"Friend request accepted: {response.message}")
    except Exception as e:
        print(f"Failed to accept friend request: {e}")
    
    # Get friends list
    try:
        response = client.get_friends()
        print(f"Friends: {', '.join(response.friends)}")
    except Exception as e:
        print(f"Failed to get friends: {e}")


def example_group_operations():
    """Example: Group operations."""
    
    client = APIClient(host="192.168.100.44", port=8080)
    # Assume we're already authenticated
    client.set_token("your_jwt_token_here")
    
    # Create a new group
    try:
        response = client.create_group(group_name="Study Group")
        group_id = response.groupId
        print(f"Group created with ID: {group_id}")
    except Exception as e:
        print(f"Failed to create group: {e}")
        return
    
    # Add a member to the group
    try:
        response = client.add_member_to_group(
            group_id=group_id,
            username="jane_doe"
        )
        print(f"Member added: {response.message}")
    except Exception as e:
        print(f"Failed to add member: {e}")
    
    # Get group details
    try:
        response = client.get_group_details(group_id=group_id)
        if response.group:
            print(f"Group: {response.group.name}")
            print(f"Members: {len(response.group.members)}")
    except Exception as e:
        print(f"Failed to get group details: {e}")
    
    # Get group members
    try:
        response = client.get_group_members(group_id=group_id)
        print("Group members:")
        for member in response.members:
            print(f"  - {member.username} (UUID: {member.uuid})")
    except Exception as e:
        print(f"Failed to get group members: {e}")
    
    # Update group name
    try:
        response = client.update_group_name(
            group_id=group_id,
            new_name="Advanced Study Group"
        )
        print(f"Group name updated: {response.message}")
    except Exception as e:
        print(f"Failed to update group name: {e}")
    
    # Get all user groups
    try:
        response = client.get_user_groups()
        print(f"User belongs to {len(response.groups)} group(s)")
        for group in response.groups:
            print(f"  - {group.name} (ID: {group.groupId})")
    except Exception as e:
        print(f"Failed to get user groups: {e}")


def example_direct_model_usage():
    """Example: Using Pydantic models directly for validation."""
    
    # Validate authentication request
    auth_req = AuthRequest(username="john_doe", password="secure123")
    print(f"Auth request data: {auth_req.model_dump()}")
    
    # Validate registration request
    reg_req = RegisterRequest(username="jane_doe", password="secure456")
    print(f"Register request data: {reg_req.model_dump()}")
    
    # Convert to JSON with aliases
    group_req = CreateGroupRequest(groupName="My Group")
    print(f"Group request JSON: {group_req.model_dump(by_alias=True)}")
    
    # Parse response
    response_data = {
        "code": 200,
        "message": "Success",
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    from frontend.src.pydantic_classes.api import AuthResponse
    auth_response = AuthResponse(**response_data)
    print(f"Token from response: {auth_response.token}")


if __name__ == "__main__":
    print("=== Authentication Examples ===")
    example_authentication()
    
    print("\n=== Friendship Examples ===")
    example_friendship_operations()
    
    print("\n=== Group Examples ===")
    example_group_operations()
    
    print("\n=== Direct Model Usage ===")
    example_direct_model_usage()
