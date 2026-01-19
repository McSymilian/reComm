"""New group dialog component."""

import customtkinter as ctk
from typing import Callable, Optional
from ..utils.api_client import APIClient


class NewGroupDialog(ctk.CTkToplevel):
    """Dialog for creating a new group."""
    
    def __init__(
        self,
        master,
        api_client: APIClient,
        on_group_created: Optional[Callable[[str, str], None]] = None,
        **kwargs
    ):
        super().__init__(master, **kwargs)
        
        self.api_client = api_client
        self.on_group_created = on_group_created
        
        self.title("Create New Group")
        self.geometry("300x200")
        self.resizable(False, False)
        
        self.transient(master)
        self.grab_set()
        
        self._setup_ui()
        
        self.update_idletasks()
        root = master.winfo_toplevel()
        x = root.winfo_x() + (root.winfo_width() - self.winfo_width()) // 2
        y = root.winfo_y() + (root.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")
    
    def _setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        
        name_label = ctk.CTkLabel(self, text="Group Name:")
        name_label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")
        
        self.name_entry = ctk.CTkEntry(self, width=260)
        self.name_entry.grid(row=1, column=0, padx=20, pady=5)
        self.name_entry.bind("<Return>", lambda e: self._create_group())
        
        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.grid(row=2, column=0, padx=20, pady=5)
        
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.grid(row=3, column=0, pady=10)
        
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            width=80,
            command=self.destroy
        )
        cancel_btn.grid(row=0, column=0, padx=10)
        
        self.create_btn = ctk.CTkButton(
            buttons_frame,
            text="Create",
            width=80,
            command=self._create_group
        )
        self.create_btn.grid(row=0, column=1, padx=10)
        
        self.name_entry.focus()
    
    def _create_group(self):
        group_name = self.name_entry.get().strip()
        
        if not group_name:
            self.error_label.configure(text="Please enter a group name")
            return
        
        self.create_btn.configure(state="disabled")
        
        try:
            response = self.api_client.create_group(group_name)
            if response.code == 200 and response.groupId:
                if self.on_group_created:
                    self.on_group_created(response.groupId, group_name)
                self.destroy()
            else:
                self.error_label.configure(text=response.message or "Failed to create group")
        except Exception as e:
            self.error_label.configure(text=f"Error: {str(e)}")
        finally:
            if self.winfo_exists():
                self.create_btn.configure(state="normal")

