"""UI component for chat view."""

import customtkinter as ctk
from typing import Optional
from datetime import datetime
from ..utils.api_client import APIClient
from ..utils.data_store import DataStore
from ..pydantic_classes.api.message import MessageModel, MessageType
import time

class ConversationFrame(ctk.CTkFrame):
    """Chat view frame for displaying and sending messages."""
    
    def __init__(
        self,
        master,
        api_client: APIClient,
        data_store: DataStore,
        **kwargs
    ):
        super().__init__(master, **kwargs)
        
        self.api_client = api_client
        self.data_store = data_store
        self.current_conversation: Optional[str] = None
        self.current_type: Optional[str] = None
        
        self.data_store.register_ui_callback("conversations_updated", self._on_messages_updated)
        
        self._setup_ui()
    
    def _setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.header_frame = ctk.CTkFrame(self, height=50)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.header_frame.grid_columnconfigure(0, weight=1)
        
        self.header_label = ctk.CTkLabel(
            self.header_frame,
            text="Select a conversation",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.header_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.messages_frame = ctk.CTkScrollableFrame(self)
        self.messages_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.messages_frame.grid_columnconfigure(0, weight=1)
        
        self.input_frame = ctk.CTkFrame(self, height=50)
        self.input_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        self.input_frame.grid_columnconfigure(0, weight=1)
        
        self.message_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Type a message..."
        )
        self.message_entry.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.message_entry.bind("<Return>", lambda e: self._send_message())
        
        self.send_button = ctk.CTkButton(
            self.input_frame,
            text="Send",
            width=80,
            command=self._send_message
        )
        self.send_button.grid(row=0, column=1, padx=10, pady=10)
        
        self._set_input_enabled(False)
    
    def _on_messages_updated(self, data=None):
        if self.current_conversation:
            self.after(0, self._refresh_messages)
    
    def load_conversation(self, identifier: str, conv_type: str):
        self.current_conversation = identifier
        self.current_type = conv_type

        chat_title = identifier if conv_type == "private" else list(filter(lambda group: group.groupId == identifier, self.data_store.groups))[0].name
        if conv_type == "private":
            prefix = "👩" if identifier.endswith("a") else "👨"
        else:
            prefix = "👹" if chat_title == "shramogus" else "👥"
        self.header_label.configure(text=f"{prefix} {chat_title}")
        
        self._set_input_enabled(True)
        
        self._refresh_messages()
    
    def _refresh_messages(self):
        for widget in self.messages_frame.winfo_children():
            widget.destroy()
        
        if not self.current_conversation:
            return
        
        if self.current_type == "private":
            messages = self.data_store.conversations.get(self.current_conversation, [])
        else:
            messages = self.data_store.group_conversations.get(self.current_conversation, [])
        
        if not messages:
            placeholder = ctk.CTkLabel(
                self.messages_frame,
                text="Say hi 👋",
                text_color="gray",
                font=ctk.CTkFont(size=16)
            )
            placeholder.grid(row=0, column=0, sticky="nsew", pady=100)
            self.messages_frame.grid_rowconfigure(0, weight=1)
            return
        
        last_is_own = None
        for i, msg in enumerate(messages):
            last_is_own = self._add_message_widget(msg, i, last_is_own)
        
        self.after(100, lambda: self.messages_frame._parent_canvas.yview_moveto(1.0))
    
    def _add_message_widget(self, message, row: int, last_is_own: bool):
        sender = message.senderName if hasattr(message, 'senderName') else "Unknown"
        content = message.content if hasattr(message, 'content') else str(message)
        timestamp = message.sentAt if hasattr(message, 'sentAt') else 0
        
        try:
            time_str = datetime.fromtimestamp(timestamp).strftime("%H:%M")
        except:
            time_str = ""
        
        is_own = sender == self.api_client.username
        
        msg_frame = ctk.CTkFrame(
            self.messages_frame,
            fg_color=("gray85", "gray20") if is_own else ("gray95", "gray30")
        )
        msg_frame.grid(
            row=row, 
            column=0, 
            sticky="e" if is_own else "w",
            padx=10,
            pady=2
        )
        
        if not is_own and last_is_own != False:
            sender_label = ctk.CTkLabel(
                msg_frame,
                text=sender,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=("gray40", "gray60")
            )
            sender_label.grid(row=0, column=0, sticky="w", padx=8, pady=(2, 0))
        
        content_label = ctk.CTkLabel(
            msg_frame,
            text=content,
            wraplength=300,
            justify="left"
        )
        content_label.grid(row=1 if not is_own else 0, column=0, sticky="w", padx=8, pady=1)
        
        time_label = ctk.CTkLabel(
            msg_frame,
            text=time_str,
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray50")
        )
        time_label.grid(row=2 if not is_own else 1, column=0, sticky="e", padx=8, pady=(0, 2))

        return is_own
    
    def _send_message(self):
        if not self.current_conversation:
            return
        
        content = self.message_entry.get().strip()
        if not content:
            return
        
        self.message_entry.delete(0, "end")
        self.send_button.configure(state="disabled")
        
        try:
            if self.current_type == "private":
                response = self.api_client.send_private_message(
                    self.current_conversation, 
                    content
                )
                
            else:
                response = self.api_client.send_group_message(
                    self.current_conversation,
                    content
                )
            
            if response.code == 200:
                self.data_store.add_message_to_conversation(
                    self.current_conversation,
                    MessageModel(
                        content=content,
                        senderName=self.api_client.username,
                        messageId=response.messageId,
                        sentAt=int(time.time()),
                        type=MessageType.PRIVATE if self.current_type == "private" else MessageType.GROUP
                    )
                )
                self._refresh_messages()
        except Exception as e:
            print(f"Error sending message: {e}")
        finally:
            self.send_button.configure(state="normal")
    
    def _set_input_enabled(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        self.message_entry.configure(state=state)
        self.send_button.configure(state=state)
    
    def clear(self):
        self.current_conversation = None
        self.current_type = None
        self.header_label.configure(text="Select a conversation")
        self._set_input_enabled(False)
        
        for widget in self.messages_frame.winfo_children():
            widget.destroy()
