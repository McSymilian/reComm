"""Main screen component - layout with sidebar and content area."""

import customtkinter as ctk
from typing import Optional
from ..utils.api_client import APIClient
from ..utils.data_store import DataStore
from .conversation_list import ConversationList
from .conversation_frame import ConversationFrame
from .friend_requests_frame import FriendRequestsFrame
from .new_group_dialog import NewGroupDialog


class MainScreen(ctk.CTkFrame):
    """Main application screen after login."""
    
    def __init__(
        self,
        master,
        username: str,
        api_client: APIClient,
        data_store: DataStore,
        **kwargs
    ):
        super().__init__(master, **kwargs)
        
        self.username = username
        self.api_client = api_client
        self.data_store = data_store
        
        self._setup_ui()
    
    def _setup_ui(self):
        self.grid_columnconfigure(0, weight=0, minsize=250)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.sidebar = ctk.CTkFrame(self, width=250)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=(5, 2), pady=5)
        self.sidebar.grid_rowconfigure(0, weight=1)
        self.sidebar.grid_columnconfigure(0, weight=1)
        
        self.conversation_list = ConversationList(
            self.sidebar,
            data_store=self.data_store,
            api_client=self.api_client,
            on_select_conversation=self._on_conversation_selected
        )
        self.conversation_list.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        self.actions_frame = ctk.CTkFrame(self.sidebar)
        self.actions_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.actions_frame.grid_columnconfigure((0, 1), weight=1)
        
        add_friend_btn = ctk.CTkButton(
            self.actions_frame,
            text="➕ Add Friend",
            command=self._show_add_friend_dialog
        )
        add_friend_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        create_group_btn = ctk.CTkButton(
            self.actions_frame,
            text="👥 New Group",
            command=self._show_create_group_dialog
        )
        create_group_btn.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        requests_btn = ctk.CTkButton(
            self.actions_frame,
            text="📬 Friend Requests",
            command=self._show_friend_requests
        )
        requests_btn.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=(2, 5), pady=5)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
        
        self.conversation_frame = ConversationFrame(
            self.content_frame,
            api_client=self.api_client,
            data_store=self.data_store
        )
        self.conversation_frame.grid(row=0, column=0, sticky="nsew")
        
        self.friend_requests_frame: Optional[FriendRequestsFrame] = None
        
        self._current_view = "conversation"
    
    def _on_conversation_selected(self, identifier: str, conv_type: str):
        if self._current_view != "conversation":
            self._show_conversation_view()
        
        self.conversation_frame.load_conversation(identifier, conv_type)
    
    def _show_conversation_view(self):
        """Show the conversation view."""
        if self.friend_requests_frame:
            self.friend_requests_frame.grid_forget()
        self.conversation_frame.grid(row=0, column=0, sticky="nsew")
        self._current_view = "conversation"
    
    def _show_friend_requests(self):
        """Show the friend requests view."""
        self.conversation_frame.grid_forget()
        
        if not self.friend_requests_frame:
            self.friend_requests_frame = FriendRequestsFrame(
                self.content_frame,
                api_client=self.api_client,
                data_store=self.data_store
            )
        
        self.friend_requests_frame.grid(row=0, column=0, sticky="nsew")
        self.friend_requests_frame.refresh()
        self._current_view = "requests"
    
    def _show_add_friend_dialog(self):
        """Show dialog to add a friend."""
        dialog = ctk.CTkInputDialog(
            text="Enter username to add:",
            title="Add Friend"
        )
        username = dialog.get_input()
        
        if username and username.strip():
            try:
                response = self.api_client.send_friend_request(username.strip())
                if response.code == 200:
                    self._show_message("Friend request sent!")
                else:
                    self._show_message(f"Failed: {response.message or 'Unknown error'}")
            except Exception as e:
                self._show_message(f"Error: {str(e)}")
    
    def _show_create_group_dialog(self):
        """Show dialog to create a group."""
        NewGroupDialog(
            self,
            api_client=self.api_client,
            on_group_created=self._on_group_created
        )
    
    def _on_group_created(self, group_id: str, group_name: str):
        """Handle group creation."""
        # Refresh groups data
        try:
            groups_response = self.api_client.get_user_groups()
            if groups_response.code == 200:
                self.data_store.groups = groups_response.groups
                self.conversation_list.refresh()
                self._show_message(f"Group '{group_name}' created!")
        except Exception as e:
            print(f"Error refreshing groups: {e}")
    
    def _show_message(self, message: str):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Message")
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        
        dialog.update_idletasks()
        root = self.winfo_toplevel()
        x = root.winfo_x() + (root.winfo_width() - dialog.winfo_width()) // 2
        y = root.winfo_y() + (root.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        label = ctk.CTkLabel(dialog, text=message, wraplength=250)
        label.pack(pady=20)
        
        btn = ctk.CTkButton(dialog, text="OK", command=dialog.destroy)
        btn.pack(pady=10)
