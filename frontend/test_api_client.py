from src.utils.api_client import APIClient
from src.pydantic_classes.api.auth import (
    AuthRequest, AuthResponse,
    RegisterRequest, RegisterResponse
)

if __name__ == "__main__":
    # Example usage of the APIClient
    client = APIClient(host="192.168.100.44", port=8080)
    client2 = APIClient(host="192.168.100.44", port=8080)
    
    # Authenticate a user
    client.authenticate(username="test", password="pass")
    client2.authenticate(username="test1", password="pass")
    
    client.send_friend_request(addressee_username="test1")
    requests = client2.get_pending_requests()
    print(f"Pending requests for test: {requests}")
    if requests.pendingRequests:
        for req in requests.pendingRequests:
            print(f"Accepting friend request from: {req.requester}")
            client2.accept_friend_request(requester=req.requester)
    message_response = client2.send_private_message(
        receiver_username="test",
        content="Hello from test_api_client!"
    )

    # group_creation_response = client.create_group(
    #     group_name="Test Group",
    # )
    # print(f"Group creation response: {group_creation_response}")

    print(client.get_notification(10))
    print(f"Message send response: {message_response}")
    # add friend
    # send_friend_request_response = client.send_friend_request(addressee_username="test")
    # if send_friend_request_response.code != 200:
    #     print(f"Add friend failed: {send_friend_request_response.message}")
    # else:
    #     print("Friend request sent successfully.")

    