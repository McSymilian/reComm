"""Friend requests frame component."""

import customtkinter as ctk
from ..utils.api_client import APIClient
from ..utils.data_store import DataStore


class FriendRequestsFrame(ctk.CTkFrame):
    """Frame for managing pending friend requests."""
    
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
        self._request_widgets: dict[str, ctk.CTkFrame] = {}
        
        # Register for DataStore updates
        self.data_store.register_ui_callback("requests_updated", self._on_requests_updated)
        
        self._setup_ui()
        self.refresh()
    
    def _setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        header = ctk.CTkLabel(
            self,
            text="Friend Requests",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        header.grid(row=0, column=0, sticky="w", padx=15, pady=15)
        
        self.requests_frame = ctk.CTkScrollableFrame(self)
        self.requests_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.requests_frame.grid_columnconfigure(0, weight=1)
    
    def _on_requests_updated(self, data=None):
        """Callback when requests data changes."""
        self.after(0, self.refresh)
    
    def refresh(self):
        for widget in self._request_widgets.values():
            widget.destroy()
        self._request_widgets.clear()
        
        for widget in self.requests_frame.winfo_children():
            widget.destroy()
        
        requests = self.data_store.get_friend_requests()
        
        if not requests:
            no_requests = ctk.CTkLabel(
                self.requests_frame,
                text="No pending friend requests",
                text_color="gray"
            )
            no_requests.grid(row=0, column=0, pady=20)
            return
        
        for i, request in enumerate(requests):
            if hasattr(request, 'requester'):
                requester = request.requester
            else:
                requester = str(request)
            self._add_request_widget(requester, i)
    
    def _add_request_widget(self, requester: str, row: int):
        request_frame = ctk.CTkFrame(self.requests_frame)
        request_frame.grid(row=row, column=0, sticky="ew", padx=5, pady=5)
        request_frame.grid_columnconfigure(0, weight=1)
        
        name_label = ctk.CTkLabel(
            request_frame,
            text=f"👤 {requester}",
            font=ctk.CTkFont(size=14)
        )
        name_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        
        buttons_frame = ctk.CTkFrame(request_frame, fg_color="transparent")
        buttons_frame.grid(row=0, column=1, padx=10, pady=10)
        
        accept_btn = ctk.CTkButton(
            buttons_frame,
            text="Accept",
            width=80,
            fg_color="green",
            hover_color="darkgreen",
            command=lambda r=requester: self._accept_request(r)
        )
        accept_btn.grid(row=0, column=0, padx=5)
        
        reject_btn = ctk.CTkButton(
            buttons_frame,
            text="Reject",
            width=80,
            fg_color="red",
            hover_color="darkred",
            command=lambda r=requester: self._reject_request(r)
        )
        reject_btn.grid(row=0, column=1, padx=5)
        
        self._request_widgets[requester] = request_frame
    
    def _accept_request(self, requester: str):
        """Accept a friend request."""
        try:
            response = self.api_client.accept_friend_request(requester)
            if response.code == 200:
                # Update local data
                self.data_store.add_friend(requester)
                # Remove from requests
                requests = [r for r in self.data_store.get_friend_requests() 
                           if (r.requester if hasattr(r, 'requester') else str(r)) != requester]
                self.data_store.set_friend_requests(requests)
                self.refresh()
        except Exception as e:
            print(f"Error accepting request: {e}")
    
    def _reject_request(self, requester: str):
        """Reject a friend request."""
        try:
            response = self.api_client.reject_friend_request(requester)
            if response.code == 200:
                # Remove from requests
                requests = [r for r in self.data_store.get_friend_requests()
                           if (r.requester if hasattr(r, 'requester') else str(r)) != requester]
                self.data_store.set_friend_requests(requests)
                self.refresh()
        except Exception as e:
            print(f"Error rejecting request: {e}")
