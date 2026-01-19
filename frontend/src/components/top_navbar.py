"""Top navigation bar component."""

import customtkinter as ctk
from typing import Callable


class TopNavbar(ctk.CTkFrame):
    """Top navigation bar with username and logout button."""
    
    def __init__(
        self,
        master,
        username: str,
        on_logout: Callable[[], None],
        **kwargs
    ):
        super().__init__(master, height=50, **kwargs)
        
        self.username = username
        self.on_logout = on_logout
        
        self._setup_ui()
    
    def _setup_ui(self):
        self.grid_columnconfigure(1, weight=1)
        
        title = ctk.CTkLabel(
            self,
            text="reComm",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.grid(row=0, column=0, padx=15, pady=10)
        
        spacer = ctk.CTkLabel(self, text="")
        spacer.grid(row=0, column=1, sticky="ew")
        
        user_label = ctk.CTkLabel(
            self,
            text=f"Welcome, {self.username}",
            font=ctk.CTkFont(size=12)
        )
        user_label.grid(row=0, column=2, padx=10, pady=10)
        
        logout_button = ctk.CTkButton(
            self,
            text="Logout",
            width=80,
            command=self.on_logout
        )
        logout_button.grid(row=0, column=3, padx=15, pady=10)
