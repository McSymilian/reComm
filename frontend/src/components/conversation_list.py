
import customtkinter as ctk
import datetime
from typing import Callable, Optional
from ..utils.data_store import DataStore
from ..utils.api_client import APIClient
from .group_actions_dialog import GroupActionsDialog


class ConversationList(ctk.CTkScrollableFrame):
    
    def __init__(
        self,
        master,
        data_store: DataStore,
        api_client: APIClient,
        on_select_conversation: Callable[[str, str], None],  # (name, type)
        **kwargs
    ):
        super().__init__(master, **kwargs)
        
        self.data_store = data_store
        self.api_client = api_client
        self.on_select_conversation = on_select_conversation
        self.selected_item: Optional[str] = None
        self._conversation_widgets: dict[str, ctk.CTkFrame] = {}
        
        self.data_store.register_ui_callback("friends_updated", self._on_data_updated)
        self.data_store.register_ui_callback("groups_updated", self._on_data_updated)
        
        self._setup_ui()
        self.refresh()
    
    def _setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
    
    def _on_data_updated(self, data=None):
        self.after(0, self.refresh)
    
    def refresh(self):
        for widget in self._conversation_widgets.values():
            widget.destroy()
        self._conversation_widgets.clear()
        
        for widget in self.winfo_children():
            widget.destroy()
        
        row = 0
        
        friends_header_frame = ctk.CTkFrame(self, fg_color="transparent")
        friends_header_frame.grid(row=row, column=0, sticky="ew", padx=5, pady=(10, 5))
        friends_header_frame.grid_columnconfigure(0, weight=1)
        
        friends_header = ctk.CTkLabel(
            friends_header_frame,
            text="Friends",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        friends_header.grid(row=0, column=0, sticky="w")
        
        friends_refresh_btn = ctk.CTkButton(
            friends_header_frame,
            text="🔄",
            width=30,
            height=24,
            fg_color="transparent",
            hover_color=("gray70", "gray30"),
            command=self._refresh_friends_and_conversations
        )
        friends_refresh_btn.grid(row=0, column=1, padx=2)
        row += 1
        
        friends = self.data_store.get_friends()
        for friend in friends:
            frame = self._create_friend_widget(friend, row)
            self._conversation_widgets[f"private:{friend}"] = frame
            row += 1
        
        if not friends:
            no_friends = ctk.CTkLabel(self, text="No friends yet", text_color="gray")
            no_friends.grid(row=row, column=0, sticky="w", padx=20, pady=2)
            row += 1
        
        groups_header_frame = ctk.CTkFrame(self, fg_color="transparent")
        groups_header_frame.grid(row=row, column=0, sticky="ew", padx=5, pady=(15, 5))
        groups_header_frame.grid_columnconfigure(0, weight=1)
        
        groups_header = ctk.CTkLabel(
            groups_header_frame,
            text="Groups",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        groups_header.grid(row=0, column=0, sticky="w")
        
        refresh_btn = ctk.CTkButton(
            groups_header_frame,
            text="🔄",
            width=30,
            height=24,
            fg_color="transparent",
            hover_color=("gray70", "gray30"),
            command=self._refresh_groups_and_conversations
        )
        refresh_btn.grid(row=0, column=1, padx=2)
        row += 1
        
        groups = getattr(self.data_store, 'groups', [])
        for group in groups:
            frame = self._create_group_widget(group, row)
            self._conversation_widgets[f"group:{group.groupId}"] = frame
            row += 1
        
        if not groups:
            no_groups = ctk.CTkLabel(self, text="No groups yet", text_color="gray")
            no_groups.grid(row=row, column=0, sticky="w", padx=20, pady=2)
    
    def _create_friend_widget(self, friend: str, row: int) -> ctk.CTkFrame:
        key = f"private:{friend}"
        
        btn = ctk.CTkButton(
            self,
            text=f"{"👩" if friend.endswith("a") else "👨"} {friend}",
            anchor="w",
            fg_color="transparent" if key != self.selected_item else ("gray75", "gray25"),
            command=lambda f=friend: self._select_conversation(f, "private", f)
        )
        btn.grid(row=row, column=0, sticky="ew", padx=5, pady=2)
        return btn
    
    def _create_group_widget(self, group, row: int) -> ctk.CTkFrame:
        group_name = group.name 
        group_id = group.groupId 
        key = f"group:{group_id}"
        
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.grid(row=row, column=0, sticky="ew", padx=5, pady=2)
        frame.grid_columnconfigure(0, weight=1)
        
        btn = ctk.CTkButton(
            frame,
            text=f"{"👹" if group_name == "shramogus" else "👥"} {group_name}",
            anchor="w",
            fg_color="transparent" if key != self.selected_item else ("gray75", "gray25"),
            command=lambda: self._select_conversation(group_id, "group", group_name)
        )
        btn.grid(row=0, column=0, sticky="ew")
        
        menu_btn = ctk.CTkButton(
            frame,
            text="☰",
            width=30,
            fg_color="transparent",
            hover_color=("gray70", "gray30"),
            command=lambda g=group: self._show_group_actions(g)
        )
        menu_btn.grid(row=0, column=1, padx=2)
        
        frame.main_button = btn
        
        return frame
    
    def _show_group_actions(self, group):
        GroupActionsDialog(
            self.winfo_toplevel(),
            api_client=self.api_client,
            data_store=self.data_store,
            group=group,
            on_group_updated=self.refresh,
            on_group_left=self._on_group_left
        )
    
    def _on_group_left(self):
        groups_response = self.api_client.get_user_groups()
        if groups_response.code == 200:
            self.data_store.groups = groups_response.groups
            self.refresh()

    def _refresh_friends_and_conversations(self):
        try:
            friends_response = self.api_client.get_friends()
            if friends_response.code == 200:
                self.data_store.set_friends(friends_response.friends)
                
                message_cutoff = int((datetime.datetime.now() - datetime.timedelta(days=3)).timestamp())
                for friend in friends_response.friends:
                    messages = self.api_client.get_private_messages_paginated(
                        friend, 
                        since=message_cutoff, 
                        total_limit=50
                    )
                    self.data_store.conversations[friend] = list(
                        sorted(messages, key=lambda msg: msg.sentAt)
                    )
                
                self.refresh()
        except Exception as e:
            print(f"Error refreshing friends: {e}")
    
    def _refresh_groups_and_conversations(self):
        groups_response = self.api_client.get_user_groups()
        if groups_response.code == 200:
            self.data_store.groups = groups_response.groups
            
            # Refresh group conversations
            message_cutoff = int((datetime.datetime.now() - datetime.timedelta(days=3)).timestamp())
            for group in self.data_store.groups:
                messages = self.api_client.get_group_messages_paginated(
                    group.groupId, 
                    since=message_cutoff, 
                    total_limit=50
                )
                self.data_store.group_conversations[group.groupId] = list(
                    sorted(messages, key=lambda msg: msg.sentAt)
                )
            
            self.refresh()

    
    def _select_conversation(self, identifier: str, conv_type: str, name: str):
        key = f"{conv_type}:{identifier}"
        
        if self.selected_item and self.selected_item in self._conversation_widgets:
            widget = self._conversation_widgets[self.selected_item]
            if hasattr(widget, 'main_button'):
                widget.main_button.configure(fg_color="transparent")
            elif hasattr(widget, 'configure'):
                widget.configure(fg_color="transparent")
        
        self.selected_item = key
        if key in self._conversation_widgets:
            widget = self._conversation_widgets[key]
            if hasattr(widget, 'main_button'):
                widget.main_button.configure(fg_color=("gray75", "gray25"))
            elif hasattr(widget, 'configure'):
                widget.configure(fg_color=("gray75", "gray25"))
        
        self.on_select_conversation(identifier, conv_type)

