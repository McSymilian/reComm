import customtkinter as ctk
from ..pydantic_classes.api.friendship import GetFriendsResponse
from .conversation_frame import ConversationFrame

from .gradient_text import CTkGradientLabel
from .conversations_bar import ConversationsBar

class MainScreen(ctk.CTkFrame):
    def __init__(self, master, username, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.conv_bar = ConversationsBar(self, conversations=["Conversation 1", "Conversation 2", "Conversation 3"])
        self.conv_bar.grid(row=0, column=0, sticky="nsw")
        
        self.conversation_frame = ConversationFrame(
            self, conversation_name="Conversation 1", 
            conversation=[("user", "Hello!"), ("bot", "Hi there!"), ("user", "How are you?"), ("bot", "I'm good, thanks!")])
        self.conversation_frame.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)


        # self.welcome_label = ctk.CTkLabel(self, text=f"Welcome, {username}!", font=("Arial", 24))
        # self.welcome_label.grid(row=0, column=1, padx=20, pady=20)