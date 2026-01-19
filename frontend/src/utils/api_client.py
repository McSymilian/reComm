"""API client for reComm backend communication."""

import logging
from typing import Optional, Dict, Any, Type, List
import json
import threading
import queue



from ..pydantic_classes.api.auth import (
    AuthBody, AuthRequest, AuthResponse, RegisterBody,
    RegisterRequest, RegisterResponse
)
from ..pydantic_classes.api.friendship import (
    SendFriendRequestRequest, SendFriendRequestResponse,
    AcceptFriendRequestRequest, AcceptFriendRequestResponse,
    RejectFriendRequestRequest, RejectFriendRequestResponse,
    GetFriendsRequest, GetFriendsResponse,
    GetPendingRequestsRequest, GetPendingRequestsResponse,
)
from ..pydantic_classes.api.group import (
    CreateGroupRequest, CreateGroupResponse,
    AddMemberToGroupRequest, AddMemberToGroupResponse,
    UpdateGroupNameRequest, UpdateGroupNameResponse,
    LeaveGroupRequest, LeaveGroupResponse,
    DeleteGroupRequest, DeleteGroupResponse,
    GetUserGroupsRequest, GetUserGroupsResponse,
    GetGroupDetailsRequest, GetGroupDetailsResponse,
    GetGroupMembersRequest, GetGroupMembersResponse,
)
from ..pydantic_classes.api.message import (
    SendGroupMessageRequest, SendGroupMessageResponse,
    GetGroupMessagesRequest, GetGroupMessagesResponse,
    SendPrivateMessageRequest, SendPrivateMessageResponse,
    GetPrivateMessagesRequest, GetPrivateMessagesResponse,
    SendMessageRequest, SendMessageResponse,
    GetRecentMessagesRequest, GetRecentMessagesResponse, MessageModel
)
from ..pydantic_classes.api.base import BaseRequestAuthenticated, BaseRequest
from .connection import Connection

logger = logging.getLogger(__name__)

class APIClient:
    """Client for communicating with the reComm backend API."""
    
    def __init__(self, host: str = "localhost", port: int = 8080, connection: Connection = None):
        """
        Initialize the API client.
        
        Args:
            host: Backend server host
            port: Backend server port
        """
        self.host = host
        self.port = port
        self.username: Optional[str] = None
        self.token: Optional[str] = None
        self.connection = connection or Connection(host, port)
        self._send_lock=threading.Lock()
        self._resp_queue: "queue.Queue[Dict[str, Any]]" = queue.Queue()
        self._notif_queue: "queue.Queue[Dict[str, Any]]" = queue.Queue()
        self._notification_callbacks: list[callable] = []
        self._running = True
        self._receiver_thread = threading.Thread(target=self._receiver_loop, daemon=True)
        self._receiver_thread.start()

    def _receiver_loop(self) -> None:
        while self._running:
            data = self.connection.receive()
            if not data:
                continue
            try:
                payload = json.loads(data.decode())
            except Exception:
                continue

            if isinstance(payload, dict) and payload.get("type", False):
                logger.info(f"Received notification: {payload}")
                self._notif_queue.put(payload)
                # Trigger all registered callbacks
                self._trigger_notification_callbacks(payload)
            else:
                logger.info(f"Received response: {payload}")
                self._resp_queue.put(payload)
    
    def _trigger_notification_callbacks(self, notification: Dict[str, Any]) -> None:
        """Trigger all registered notification callbacks."""
        for callback in self._notification_callbacks:
            try:
                callback(notification)
            except Exception as e:
                logger.error(f"Error in notification callback: {e}")
    
    def _send_request(self, request: Type[BaseRequest], timeout: float = 10.0) -> Dict[str, Any]:

        request_json = request.model_dump_json().encode()
        logger.info(f">>> REQUEST: {request_json.decode()}")
        with self._send_lock:
            self.connection.send(request_json)
            try:
                response_dict = self._resp_queue.get(timeout=timeout)
            except queue.Empty:
                logger.error("<<< RESPONSE: Timed out waiting for response")
                raise TimeoutError("Timed out waiting for response")
        logger.info(f"<<< RESPONSE: {response_dict}")
        return response_dict
    
    def _build_request(self, 
                       request_cls: Type[BaseRequestAuthenticated], 
                       **kwargs) -> BaseRequestAuthenticated:
        """
        Build a request object with optional authentication.
        
        Args:
            request_cls: Request class to instantiate
            kwargs: Additional fields for the request body
            
        Returns:
            Instance of request_cls
        """

        if not self.token:
            raise ValueError("Authentication token is not set.")
        
        body_model_cls = request_cls.model_fields['body'].annotation

        body_instance = body_model_cls.model_validate(kwargs)

        request = request_cls(
            body=body_instance,
            token=self.token)
 
        return request
    
    def register_notification_callback(self, callback: callable) -> None:
        """Register a callback to be triggered when a notification is received."""
        if callback not in self._notification_callbacks:
            self._notification_callbacks.append(callback)
        logger.info("Registered notification callback.")

    def unregister_notification_callback(self, callback: callable) -> None:
        """Unregister a notification callback."""
        if callback in self._notification_callbacks:
            self._notification_callbacks.remove(callback)
        logger.info("Unregistered notification callback.")

    def get_notification(self, timeout: Optional[float] = None) -> Optional[Dict[str, Any]]:
        """
        Fetch the next notification if available. Non-blocking when timeout=0, blocking when None.
        """
        try:
            notification: Optional[Dict[str, Any]] = self._notif_queue.get(timeout=timeout)
            logger.info(f"Received notification {notification}")
            return notification
        except queue.Empty:
            return None


    def set_token(self, token: str) -> None:
        """Set the authentication token."""
        self.token = token
    
    def clear_token(self) -> None:
        """Clear the authentication token."""
        self.token = None
    

    
    # Authentication methods
    
    def authenticate(self, username: str, password: str) -> AuthResponse:
        """
        Authenticate a user.
        
        Args:
            username: Username
            password: Password
            
        Returns:
            AuthResponse with token
        """
        body: AuthBody = AuthBody(username=username, password=password)
        request = AuthRequest(body=body)
        response = self._send_request(request)
        response_obj = AuthResponse(**response)
        if response_obj.token:
            self.username = username
            self.set_token(response_obj.token)
        return response_obj
    
    def register(self, username: str, password: str) -> RegisterResponse:
        """
        Register a new user.
        
        Args:
            username: Desired username
            password: Password
            
        Returns:
            RegisterResponse with token
        """
        body: RegisterBody = RegisterBody(username=username, password=password)
        request = RegisterRequest(body=body)
        response = self._send_request(request)
        response_obj = RegisterResponse(**response)
        if response_obj.token:
            self.set_token(response_obj.token)
            self.username = username
        return response_obj
    
    # Friendship methods
    
    def send_friend_request(self, addressee_username: str) -> SendFriendRequestResponse:
        """
        Send a friend request.
        
        Args:
            addressee_username: Username to send request to
            
        Returns:
            SendFriendRequestResponse
        """
        request = self._build_request(SendFriendRequestRequest, addresseeUsername=addressee_username)
        response = self._send_request(request)
        print(f"Send Friend Request Response: {response}")
        return SendFriendRequestResponse(**response)
    
    def accept_friend_request(self, requester: str) -> AcceptFriendRequestResponse:
        """
        Accept a friend request.
        
        Args:
            requester: Username who sent the request
            
        Returns:
            AcceptFriendRequestResponse
        """
        request = self._build_request(AcceptFriendRequestRequest, requester=requester)
        response = self._send_request(request)
        return AcceptFriendRequestResponse(**response)
    
    def reject_friend_request(self, requester: str) -> RejectFriendRequestResponse:
        """
        Reject a friend request.
        
        Args:
            requester: Username who sent the request
            
        Returns:
            RejectFriendRequestResponse
        """
        request = self._build_request(RejectFriendRequestRequest, requester=requester)
        response = self._send_request(request)
        return RejectFriendRequestResponse(**response)
    
    def get_friends(self) -> GetFriendsResponse:
        """
        Get list of friends.
        
        Returns:
            GetFriendsResponse with list of friend usernames
        """
        request = self._build_request(GetFriendsRequest)
        response = self._send_request(request)
        print(f"Get Friends Response: {response}")
        return GetFriendsResponse(**response)
    
    def get_pending_requests(self) -> GetPendingRequestsResponse:
        """
        Get list of pending friend requests.
        
        Returns:
            GetPendingRequestsResponse with pending requests
        """
        request = self._build_request(GetPendingRequestsRequest)
        response = self._send_request(request)
        print(f"Get Pending Requests Response: {response}")
        return GetPendingRequestsResponse(**response)
    
    # Group methods
    
    def create_group(self, group_name: str) -> CreateGroupResponse:
        """
        Create a new group.
        
        Args:
            group_name: Name for the new group
            
        Returns:
            CreateGroupResponse with group ID
        """
        request = self._build_request(CreateGroupRequest, groupName=group_name)
        response = self._send_request(request)
        return CreateGroupResponse(**response)
    
    def add_member_to_group(self, group_id: str, username: str) -> AddMemberToGroupResponse:
        """
        Add a member to a group.
        
        Args:
            group_id: UUID of the group
            username: Username to add
            
        Returns:
            AddMemberToGroupResponse
        """
        request = self._build_request(AddMemberToGroupRequest, groupId=group_id, username=username)
        response = self._send_request(request)
        return AddMemberToGroupResponse(**response)
    
    def update_group_name(self, group_id: str, new_name: str) -> UpdateGroupNameResponse:
        """
        Update a group's name.
        
        Args:
            group_id: UUID of the group
            new_name: New name for the group
            
        Returns:
            UpdateGroupNameResponse
        """
        request = self._build_request(UpdateGroupNameRequest, groupId=group_id, newName=new_name)
        response = self._send_request(request)
        return UpdateGroupNameResponse(**response)
    
    def leave_group(self, group_id: str) -> LeaveGroupResponse:
        """
        Leave a group.
        
        Args:
            group_id: UUID of the group to leave
            
        Returns:
            LeaveGroupResponse
        """
        request = self._build_request(LeaveGroupRequest, groupId=group_id)
        response = self._send_request(request)
        return LeaveGroupResponse(**response)
    
    def delete_group(self, group_id: str) -> DeleteGroupResponse:
        """
        Delete a group.
        
        Args:
            group_id: UUID of the group to delete
            
        Returns:
            DeleteGroupResponse
        """
        request = self._build_request(DeleteGroupRequest, groupId=group_id)
        response = self._send_request(request)
        return DeleteGroupResponse(**response)
    
    def get_user_groups(self) -> GetUserGroupsResponse:
        """
        Get all groups the user belongs to.
        
        Returns:
            GetUserGroupsResponse with list of groups
        """
        request = self._build_request(GetUserGroupsRequest)
        response = self._send_request(request)
        print(f"Get User Groups Response: {response}")
        return GetUserGroupsResponse(**response)
    
    def get_group_details(self, group_id: str) -> GetGroupDetailsResponse:
        """
        Get details of a specific group.
        
        Args:
            group_id: UUID of the group
            
        Returns:
            GetGroupDetailsResponse with group details
        """
        request = self._build_request(GetGroupDetailsRequest, groupId=group_id)
        response = self._send_request(request)
        print(f"Get Group Details Response: {response}")
        return GetGroupDetailsResponse(**response)
    
    def get_group_members(self, group_id: str) -> GetGroupMembersResponse:
        """
        Get members of a specific group.
        
        Args:
            group_id: UUID of the group
            
        Returns:
            GetGroupMembersResponse with list of members
        """
        request = self._build_request(GetGroupMembersRequest, groupId=group_id)
        response = self._send_request(request)
        return GetGroupMembersResponse(**response)

    # Message methods

    def send_group_message(self, group_id: str, content: str) -> SendGroupMessageResponse:
        """
        Send a message to a group.

        Args:
            group_id: UUID of the group
            content: Message content

        Returns:
            SendGroupMessageResponse with messageId
        """
        request = self._build_request(SendGroupMessageRequest, groupId=group_id, content=content)
        response = self._send_request(request)
        return SendGroupMessageResponse(**response)

    def get_group_messages(
        self,
        group_id: str,
        limit: int = 100,
        offset: int = 0,
        since: Optional[int] = None,
    ) -> GetGroupMessagesResponse:
        """
        Fetch messages from a group.

        Args:
            group_id: UUID of the group
            limit: Maximum number of messages
            offset: Pagination offset
            since: Optional unix timestamp to filter messages

        Returns:
            GetGroupMessagesResponse with messages and count
        """
        request = self._build_request(GetGroupMessagesRequest, groupId=group_id, limit=limit, offset=offset, since=since)
        response = self._send_request(request)
        return GetGroupMessagesResponse(**response)
    
    def get_group_messages_paginated(
        self,
        group_id: str,
        since: int,
        total_limit: int = 50,
    ) -> List[MessageModel]:
        """
        Fetch messages from a group using pagination.

        Args:
            group_id: UUID of the group
            since: Unix timestamp to fetch messages since
            total_limit: Total maximum number of messages to fetch
        """
        all_messages: List[MessageModel] = []
        offset = 0
        page_size = 5 

        while len(all_messages) < total_limit:
            limit = min(page_size, total_limit - len(all_messages))
            response = self.get_group_messages(
                group_id=group_id,
                limit=page_size,
                offset=offset,
                since=since
            )
            all_messages.extend(response.messages)
            if len(response.messages) < limit:
                break
            offset += limit

        return all_messages

    def send_private_message(self, receiver_username: str, content: str) -> SendPrivateMessageResponse:
        """
        Send a private message to another user.

        Args:
            receiver_username: Username of the receiver
            content: Message content

        Returns:
            SendPrivateMessageResponse with messageId
        """
        request = self._build_request(SendPrivateMessageRequest, receiverUsername=receiver_username, content=content)
        response = self._send_request(request)
        return SendPrivateMessageResponse(**response)

    def get_private_messages(
        self,
        other_username: str,
        limit: int = 10,
        offset: int = 0,
        since: Optional[int] = None,
    ) -> GetPrivateMessagesResponse:
        """
        Fetch private messages with a specific user.

        Args:
            other_username: The other participant's username
            limit: Maximum number of messages
            offset: Pagination offset
            since: Optional unix timestamp

        Returns:
            GetPrivateMessagesResponse with messages and count
        """
        request = self._build_request(GetPrivateMessagesRequest, otherUsername=other_username, limit=limit, offset=offset, since=since)
        response = self._send_request(request)
        return GetPrivateMessagesResponse(**response)

    def get_private_messages_paginated(
        self,
        other_username: str,
        since: int,
        total_limit: int = 50,
    ) -> List[MessageModel]:
        """
        Fetch private messages with a specific user using pagination.

        Args:
            other_username: The other participant's username
            since: Unix timestamp to fetch messages since
            total_limit: Total maximum number of messages to fetch

        Returns:
            List of MessageModel
        """
        all_messages: List[MessageModel] = []
        offset = 0
        page_size = 5 # Number of messages to fetch per request

        while len(all_messages) < total_limit:
            limit = min(page_size, total_limit - len(all_messages))
            response = self.get_private_messages(
                other_username=other_username,
                limit=page_size,
                offset=offset,
                since=since
            )
            all_messages.extend(response.messages)
            if len(response.messages) < limit:
                break
            offset += limit

        return all_messages
        
    def send_message(self, group_id: str, content: str) -> SendMessageResponse:
        """
        Send a message via the generic SEND_MESSAGE endpoint (group-based).

        Args:
            group_id: UUID of the group
            content: Message content

        Returns:
            SendMessageResponse with messageId
        """
        request = self._build_request(SendMessageRequest, groupId=group_id, content=content)
        response = self._send_request(request)
        return SendMessageResponse(**response)

    def get_recent_messages(self, group_id: str, limit: int = 100) -> GetRecentMessagesResponse:
        """
        Fetch recent messages from a group (default last 30 days on backend).

        Args:
            group_id: UUID of the group
            limit: Maximum number of messages

        Returns:
            GetRecentMessagesResponse with messages and count
        """
        request = self._build_request(GetRecentMessagesRequest, groupId=group_id, limit=limit)
        response = self._send_request(request)
        return GetRecentMessagesResponse(**response)

    def close(self) -> None:
        """Stop receiver thread and close the connection."""
        self._running = False
        if self._receiver_thread.is_alive():
            self._receiver_thread.join(timeout=1.0)
        self.connection.close()

if __name__ == "__main__":
    client = APIClient(host="192.168.100.44", port=8080)
    auth_response = client.authenticate(username="test", password="pass")
    print(f"Authenticated! Token: {auth_response.token}")
    print(client.get_pending_requests())
    print(client.get_friends())
    groups = client.get_user_groups()
    print(client.get_user_groups())
    print(client.get_private_messages(other_username="nowy_user"))

    client.set_token(auth_response.token)
