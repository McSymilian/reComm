"""Login/Registration frame."""

import customtkinter as ctk
from typing import Callable
from ..utils.api_client import APIClient


class LoginFrame(ctk.CTkFrame):
    def __init__(
        self,
        master,
        api_client: APIClient,
        on_login_success: Callable[[str], None],
        **kwargs
    ):
        super().__init__(master, **kwargs)
        
        self.api_client = api_client
        self.on_login_success = on_login_success
        
        self._setup_ui()
    
    def _setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        container = ctk.CTkFrame(self)
        container.grid(row=0, column=0)
        
        title = ctk.CTkLabel(
            container,
            text="reComm",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, pady=(0, 30))
        
        username_label = ctk.CTkLabel(container, text="Username:")
        username_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        
        self.username_entry = ctk.CTkEntry(container, width=200)
        self.username_entry.grid(row=1, column=1, padx=10, pady=5)
        
        password_label = ctk.CTkLabel(container, text="Password:")
        password_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        
        self.password_entry = ctk.CTkEntry(container, width=200, show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=5)
        
        self.error_label = ctk.CTkLabel(
            container,
            text="",
            text_color="red"
        )
        self.error_label.grid(row=3, column=0, columnspan=2, pady=5)
        
        buttons_frame = ctk.CTkFrame(container, fg_color="transparent")
        buttons_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        self.login_button = ctk.CTkButton(
            buttons_frame,
            text="Login",
            command=self._handle_login
        )
        self.login_button.grid(row=0, column=0, padx=10)
        
        self.register_button = ctk.CTkButton(
            buttons_frame,
            text="Register",
            command=self._handle_register
        )
        self.register_button.grid(row=0, column=1, padx=10)
        
        self.password_entry.bind("<Return>", lambda e: self._handle_login())
    
    def _get_credentials(self) -> tuple[str, str]:
        return self.username_entry.get().strip(), self.password_entry.get()
    
    def _show_error(self, message: str):
        self.error_label.configure(text=message)
    
    def _clear_error(self):
        self.error_label.configure(text="")
    
    def _handle_login(self):
        username, password = self._get_credentials()
        
        if not username or not password:
            self._show_error("Please enter username and password")
            return
        
        self._clear_error()
        self.login_button.configure(state="disabled")
        self.register_button.configure(state="disabled")
        
        try:
            response = self.api_client.authenticate(username, password)

            if response.code == 200:
                self.on_login_success(username)
            else:
                self._show_error(response.message or "Login failed")
        except Exception as e:
            self._show_error(f"Connection error: {str(e)}")
        finally:
            if self.winfo_exists():
                self.login_button.configure(state="normal")
                self.register_button.configure(state="normal")
    
    def _handle_register(self):
        username, password = self._get_credentials()
        
        if not username or not password:
            self._show_error("Please enter username and password")
            return
        
        if len(password) < 4:
            self._show_error("Password must be at least 4 characters long")
            return
        
        self._clear_error()
        self.login_button.configure(state="disabled")
        self.register_button.configure(state="disabled")
        
        try:
            response = self.api_client.register(username, password)
            if response.code == 200:
                self.on_login_success(username)
            else:
                self._show_error(response.message or "Registration failed")
        except Exception as e:
            self._show_error(f"Connection error: {str(e)}")
        finally:
            if self.winfo_exists():
                self.login_button.configure(state="normal")
                self.register_button.configure(state="normal")
