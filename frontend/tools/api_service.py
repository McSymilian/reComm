import json
from typing import Optional
from queue import Queue

from tools.tcp_client import TCPClient

class ApiService:
    def __init__(self, host: str, port: int):
        self.tcp_client = TCPClient(host=host, port=port)
        self.response_queue: Queue = Queue()
        self.notification_queue: Queue = Queue()
        self.tcp_client.on_message = self._handle_receive
        self.tcp_client.connect()
        self.token: Optional[str] = None

    def _handle_receive(self, data: bytes):
        resp = json.loads(data.decode('utf-8'))
        if not "type" in resp:
            self.response_queue.put(resp)
        else:
            self.notification_queue.put(resp)

    def register(self, username: str, password: str) -> bool:
        self.tcp_client.send(json.dumps({
            "method": "REGISTER",
            "body": {
                "username": username,
                "password": password
            }
        }))
        response = self.response_queue.get()
        if response["code"] == 201:
            self.token = response["token"]
            return True

        return False

    def login(self, username: str, password: str) -> bool:
        self.tcp_client.send(json.dumps({
            "method": "AUTH",
            "body": {
                "username": username,
                "password": password
            }
        }))
        response = self.response_queue.get()
        if response["code"] == 200:
            self.token = response["token"]
            return True

        return False

    def send_friend_request(self, friend_username: str) -> bool:
        if not self.token:
            raise Exception("User not authenticated")

        self.tcp_client.send(json.dumps({
            "method": "SEND_FRIEND_REQUEST",
            "token": self.token,
            "body": {
                "addresseeUsername": friend_username
            }
        }))
        response = self.response_queue.get()
        return response["code"] == 200

    def accept_friend_request(self, requester_username: str) -> bool:
        if not self.token:
            raise Exception("User not authenticated")

        self.tcp_client.send(json.dumps({
            "method": "ACCEPT_FRIEND_REQUEST",
            "token": self.token,
            "body": {
                "requester": requester_username
            }
        }))
        response = self.response_queue.get()
        return response["code"] == 200

    def reject_friend_request(self, requester_username: str) -> bool:
        if not self.token:
            raise Exception("User not authenticated")

        self.tcp_client.send(json.dumps({
            "method": "REJECT_FRIEND_REQUEST",
            "token": self.token,
            "body": {
                "requester": requester_username
            }
        }))
        response = self.response_queue.get()
        return response["code"] == 200

    def get_all_friends(self) -> Optional[list[str]]:
        if not self.token:
            raise Exception("User not authenticated")

        self.tcp_client.send(json.dumps({
            "method": "GET_FRIENDS",
            "token": self.token,
            "body": {}
        }))
        response = self.response_queue.get()
        if response["code"] == 200:
            return response["friends"]

        return None

    def get_pending_friend_requests(self) -> Optional[list]:
        if not self.token:
            raise Exception("User not authenticated")

        self.tcp_client.send(json.dumps({
            "method": "GET_PENDING_REQUESTS",
            "token": self.token,
            "body": {}
        }))
        response = self.response_queue.get()
        if response["code"] == 200:
            return response["pendingRequests"]

        return None

    def create_group(self, group_name: str) -> Optional[str]:
        if not self.token:
            raise Exception("User not authenticated")

        self.tcp_client.send(json.dumps({
            "method": "CREATE_GROUP",
            "token": self.token,
            "body": {
                "groupName": group_name
            }
        }))
        response = self.response_queue.get()
        if response["code"] == 200:
            return response["groupId"]
        return None

    def add_member_to_group(self, group_id: str, username: str) -> bool:
        if not self.token:
            raise Exception("User not authenticated")

        self.tcp_client.send(json.dumps({
            "method": "ADD_MEMBER_TO_GROUP",
            "token": self.token,
            "body": {
                "groupId": group_id,
                "username": username
            }
        }))
        response = self.response_queue.get()
        return response["code"] == 200

    def change_group_name(self, group_id: str, new_name: str) -> bool:
        if not self.token:
            raise Exception("User not authenticated")

        self.tcp_client.send(json.dumps({
            "method": "UPDATE_GROUP_NAME",
            "token": self.token,
            "body": {
                "groupId": group_id,
                "newName": new_name
            }
        }))
        response = self.response_queue.get()
        return response["code"] == 200

    def leave_group(self, group_id: str) -> bool:
        if not self.token:
            raise Exception("User not authenticated")
        self.tcp_client.send(json.dumps({
            "method": "LEAVE_GROUP",
            "token": self.token,
            "body": {
                "groupId": group_id
            }
        }))
        response = self.response_queue.get()
        return response["code"] == 200

    def delete_group(self, group_id: str) -> bool:
        if not self.token:
            raise Exception("User not authenticated")
        self.tcp_client.send(json.dumps({
            "method": "DELETE_GROUP",
            "token": self.token,
            "body": {
                "groupId": group_id
            }
        }))
        response = self.response_queue.get()
        return response["code"] == 200

    def get_all_users_groups(self) -> Optional[list]:
        if not self.token:
            raise Exception("User not authenticated")
        self.tcp_client.send(json.dumps({
            "method": "GET_USER_GROUPS",
            "token": self.token,
            "body": {}
        }))
        response = self.response_queue.get()
        if response["code"] == 200:
            return response["groups"]
        return None

    def get_group_details(self, group_id: str) -> Optional[dict]:
        if not self.token:
            raise Exception("User not authenticated")
        self.tcp_client.send(json.dumps({
            "method": "GET_GROUP_DETAILS",
            "token": self.token,
            "body": {
                "groupId": group_id
            }
        }))
        response = self.response_queue.get()
        if response["code"] == 200:
            return response["group"]
        return None

    def get_group_members(self, group_id: str) -> Optional[list]:
        if not self.token:
            raise Exception("User not authenticated")
        self.tcp_client.send(json.dumps({
            "method": "GET_GROUP_MEMBERS",
            "token": self.token,
            "body": {
                "groupId": group_id
            }
        }))
        response = self.response_queue.get()
        if response["code"] == 200:
            return response["members"]
        return None

    def send_message_to_group(self, group_id: str, message: str) -> Optional[str]:
        if not self.token:
            raise Exception("User not authenticated")
        self.tcp_client.send(json.dumps({
            "method": "SEND_GROUP_MESSAGE",
            "token": self.token,
            "body": {
                "groupId": group_id,
                "content": message
            }
        }))
        response = self.response_queue.get()
        if response["code"] == 200:
            return response["messageId"]
        return None

    def get_group_messages(self, group_id: str, since = 1638360000, limit = 100, offset= 0) -> Optional[list]:
        if not self.token:
            raise Exception("User not authenticated")
        self.tcp_client.send(json.dumps({
            "method": "GET_GROUP_MESSAGES",
            "token": self.token,
            "body": {
                "groupId": group_id,
                "since": since,
                "limit": limit,
                "offset": offset
            }
        }))
        response = self.response_queue.get()
        if response["code"] == 200:
            return response["messages"]
        return None

    def send_message_to_user(self, receiver_username: str, message: str) -> Optional[str]:
        if not self.token:
            raise Exception("User not authenticated")

        self.tcp_client.send(json.dumps({
            "method": "SEND_PRIVATE_MESSAGE",
            "token": self.token,
            "body": {
                "receiverUsername": receiver_username,
                "content": message
            }
        }))
        response = self.response_queue.get()
        if response["code"] == 200:
            return response["messageId"]
        return None

    def get_private_messages(self, correspondent_username: str, since = 1638360000, limit = 100, offset= 0) -> Optional[list]:
        if not self.token:
            raise Exception("User not authenticated")

        self.tcp_client.send(json.dumps({
            "method": "GET_PRIVATE_MESSAGES",
            "token": self.token,
            "body": {
                "otherUsername": correspondent_username,
                "since": since,
                "limit": limit,
                "offset": offset
            }
        }))
        response = self.response_queue.get()
        if response["code"] == 200:
            return response["messages"]
        return None