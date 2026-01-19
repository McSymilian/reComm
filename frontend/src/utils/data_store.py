

import datetime
import logging
from src.pydantic_classes.api.message import MessageModel
from src.pydantic_classes.api.notification import (
    NotificationType, NewPrivateMessageNotificationModel, NewGroupMessageNotificationModel, FriendRequestNotificationModel
)
from src.pydantic_classes.api.friendship import FriendshipRequest
from src.pydantic_classes.api.group import Group
from .api_client import APIClient
from typing import List, Dict

logger = logging.getLogger(__name__)

class DataStore:
    def __init__(self, client):
        self.client: APIClient = client
        self.conversations: Dict[str, List[MessageModel]] = {}
        self.friend_requests: List[FriendshipRequest] = []
        self.group_conversations: Dict[str, List[MessageModel]] = {}
        self.friends: List[str] = []
        self.groups: List[Group] = []
        self.unread: set[str] = set()  # Conversation identifiers with unread messages
        
        self._ui_callbacks: dict[str, list[callable]] = {}
    
    def register_ui_callback(self, event_type: str, callback: callable) -> None:
        """Register a UI callback for a specific event type.
        
        Event types: 'friends_updated', 'conversations_updated', 
                     'requests_updated', 'groups_updated'
        """
        if event_type not in self._ui_callbacks:
            self._ui_callbacks[event_type] = []
        if callback not in self._ui_callbacks[event_type]:
            self._ui_callbacks[event_type].append(callback)
    
    def unregister_ui_callback(self, event_type: str, callback: callable) -> None:
        """Unregister a UI callback."""
        if event_type in self._ui_callbacks and callback in self._ui_callbacks[event_type]:
            self._ui_callbacks[event_type].remove(callback)
    
    def _notify_ui(self, event_type: str, data=None) -> None:
        """Notify all registered UI callbacks for an event type."""
        for callback in self._ui_callbacks.get(event_type, []):
            try:
                callback(data)
            except Exception as e:
                logger.error(f"UI callback error for {event_type}: {e}")


    def __str__(self):
        return f"DataStore(friends={self.friends}, friend_requests={self.friend_requests}, conversations={list(self.conversations.values())})"

    def update_field_state(self, field_name, new_value):
        setattr(self, field_name, new_value)

    def set_friends(self, friends_list):
        self.friends = friends_list
        self._notify_ui("friends_updated", self.friends)


    def get_friends(self):
        return self.friends
    

    def add_friend(self, friend):
        self.friends.append(friend)
        self._notify_ui("friends_updated", self.friends)
    

    def get_friend_requests(self):
        return self.friend_requests
    

    def set_friend_requests(self, requests_list):
        self.friend_requests = requests_list
        self._notify_ui("requests_updated", self.friend_requests)
    

    def add_friend_request(self, from_):
        self.friend_requests.append((from_))
        self._notify_ui("requests_updated", self.friend_requests)


    def get_conversations(self):
        return self.conversations
    

    def set_conversations(self, conversations_dict):
        self.conversations = conversations_dict
        self._notify_ui("conversations_updated", self.conversations)
    

    def add_conversation(self, conversation_name, conversation_data):
        self.conversations[conversation_name] = conversation_data
        self._notify_ui("conversations_updated", self.conversations)


    def add_message_to_conversation(self, conversation_name, message):
        if message.type == "PRIVATE":
            if conversation_name in self.conversations:
                self.conversations[conversation_name].append(message)
            else:
                self.conversations[conversation_name] = [message]
        elif message.type == "GROUP":
            if conversation_name in self.group_conversations:
                self.group_conversations[conversation_name].append(message)
            else:
                self.group_conversations[conversation_name] = [message]
        self._notify_ui("conversations_updated", self.conversations)
    

    def process_notification(self, notification: dict):
        """Process incoming notification from API client."""
        notification_type_str = notification.get('type')
        
        try:
            notification_type = NotificationType(notification_type_str)
        except (ValueError, KeyError):
            logger.error(f"Unknown notification type: {notification_type_str}")
            return
        
        if notification_type == NotificationType.NEW_PRIVATE_MESSAGE:
            try:
                notification_obj = NewPrivateMessageNotificationModel(**notification)
                logger.info(f"New private message from {notification_obj.senderName}")
                self.add_message_to_conversation(notification_obj.senderName, MessageModel(
                    messageId=notification_obj.messageId,
                    senderId=notification_obj.senderId,
                    type="PRIVATE",
                    senderName=notification_obj.senderName,
                    content=notification_obj.content,
                    sentAt=notification_obj.sentAt,
                    deliveredAt=int(datetime.datetime.now().timestamp())
                ))
            except Exception as e:
                logger.error(f"Error processing private message notification: {e}")
        
        elif notification_type == NotificationType.NEW_GROUP_MESSAGE:
            try:
                notification_obj = NewGroupMessageNotificationModel(**notification)
                logger.info(f"New group message in group {notification_obj.groupId} from {notification_obj.senderName}")
                self.add_message_to_conversation(notification_obj.groupId, MessageModel(
                    messageId=notification_obj.messageId,
                    senderId=notification_obj.senderId,
                    receiverId=notification_obj.groupId,
                    type="GROUP",
                    senderName=notification_obj.senderName,
                    content=notification_obj.content,
                    sentAt=notification_obj.sentAt,
                    deliveredAt=int(datetime.datetime.now().timestamp())
                ))
            except Exception as e:
                logger.error(f"Error processing group message notification: {e}")

        elif notification_type == NotificationType.FRIEND_REQUEST:
            try:
                notification_obj = FriendRequestNotificationModel(**notification)
                logger.info(f"New friend request from {notification_obj.requester}")
                self.add_friend_request(notification_obj.requester, notification_obj.sentAt)
            except Exception as e:
                logger.error(f"Error processing friend request notification: {e}")
        else:
            logger.warning(f"Unknown notification type received: {notification_type}")
        
        
    def initialize(self):
        message_cutoff = int((datetime.datetime.now() - datetime.timedelta(days=3)).timestamp())
        self.friends = self.client.get_friends().friends
        self.friend_requests = self.client.get_pending_requests().pendingRequests
        self.conversations = {friend: list(sorted(self.client.get_private_messages_paginated(friend, since=message_cutoff, total_limit=50), key=lambda msg: msg.sentAt)) for friend in self.friends}
        self.groups = self.client.get_user_groups().groups
        self.group_conversations = {group.groupId: list(sorted(self.client.get_group_messages_paginated(group.groupId, since=message_cutoff, total_limit=50), key=lambda msg: msg.sentAt)) for group in self.groups}
        self.client.register_notification_callback(self.process_notification)

    def reset(self):
        self.conversations = {}
        self.friend_requests = []
        self.group_conversations = {}
        self.group_requests = []

