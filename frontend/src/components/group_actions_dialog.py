"""UI component for group actions."""

import customtkinter as ctk
from typing import Callable, Optional
from ..utils.api_client import APIClient
from ..utils.data_store import DataStore
from ..pydantic_classes.api.group import Group


class GroupActionsDialog(ctk.CTkToplevel):
    """Dialog for group management actions."""
    
    def __init__(
        self,
        master,
        api_client: APIClient,
        data_store: DataStore,
        group: Group,
        on_group_updated: Optional[Callable[[], None]] = None,
        on_group_left: Optional[Callable[[], None]] = None,
        **kwargs
    ):
        super().__init__(master, **kwargs)
        
        self.api_client = api_client
        self.data_store = data_store
        self.group = group
        self.on_group_updated = on_group_updated
        self.on_group_left = on_group_left
        
        self.title(f"Group: {group.name}")
        self.geometry("450x450")
        self.resizable(False, False)
        
        self.transient(master)
        self.grab_set()
        
        self._setup_ui()
        
        self.update_idletasks()
        root = master.winfo_toplevel()
        x = root.winfo_x() + (root.winfo_width() - self.winfo_width()) // 2
        y = root.winfo_y() + (root.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")
        
        self._load_members()
    
    def _setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        
        info_frame = ctk.CTkFrame(self)
        info_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        info_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(info_frame, text="Group Name:", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, padx=10, pady=5, sticky="w"
        )
        self.name_entry = ctk.CTkEntry(info_frame, width=200)
        self.name_entry.insert(0, self.group.name)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        
        self.rename_btn = ctk.CTkButton(
            info_frame, text="Rename", width=80, command=self._rename_group
        )
        self.rename_btn.grid(row=0, column=2, padx=10, pady=5)
        
        add_frame = ctk.CTkFrame(self)
        add_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        add_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(add_frame, text="Add Member:", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, padx=10, pady=5, sticky="w"
        )
        self.member_entry = ctk.CTkEntry(add_frame, placeholder_text="Username")
        self.member_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.member_entry.bind("<Return>", lambda e: self._add_member())
        
        self.add_btn = ctk.CTkButton(
            add_frame, text="Add", width=80, command=self._add_member
        )
        self.add_btn.grid(row=0, column=2, padx=10, pady=5)
        
        ctk.CTkLabel(self, text="Members:", font=ctk.CTkFont(weight="bold")).grid(
            row=2, column=0, padx=15, pady=(10, 5), sticky="w"
        )
        
        self.members_frame = ctk.CTkScrollableFrame(self, height=150)
        self.members_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=5)
        self.members_frame.grid_columnconfigure(0, weight=1)
        
        self.status_label = ctk.CTkLabel(self, text="", text_color="gray")
        self.status_label.grid(row=4, column=0, padx=10, pady=5)
        
        actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        actions_frame.grid(row=5, column=0, pady=15)
        
        self.leave_btn = ctk.CTkButton(
            actions_frame,
            text="Leave Group",
            fg_color="orange",
            hover_color="darkorange",
            command=self._leave_group
        )
        self.leave_btn.grid(row=0, column=0, padx=10)
        
        self.delete_btn = ctk.CTkButton(
            actions_frame,
            text="Delete Group",
            fg_color="red",
            hover_color="darkred",
            command=self._delete_group
        )
        self.delete_btn.grid(row=0, column=1, padx=10)
        
        ctk.CTkButton(
            actions_frame, text="Close", width=80, command=self.destroy
        ).grid(row=0, column=2, padx=10)
    
    def _load_members(self):
        try:
            response = self.api_client.get_group_members(self.group.groupId)
            if response.code == 200:
                self._display_members(response.members)
            else:
                self._show_status(f"Failed to load members, try refreshing", "red")
        except Exception as e:
            self._show_status(f"Error: {e}", "red")
    
    def _display_members(self, members):
        for widget in self.members_frame.winfo_children():
            widget.destroy()
        
        for i, member in enumerate(members):
            username = member.username if hasattr(member, 'username') else str(member)
            member_label = ctk.CTkLabel(
                self.members_frame,
                text=f"👤 {username}",
                anchor="w"
            )
            member_label.grid(row=i, column=0, sticky="w", padx=10, pady=2)
        
        if not members:
            ctk.CTkLabel(
                self.members_frame,
                text="No members found",
                text_color="gray"
            ).grid(row=0, column=0, pady=10)
    
    def _show_status(self, message: str, color: str = "gray"):
        self.status_label.configure(text=message, text_color=color)
    
    def _rename_group(self):
        new_name = self.name_entry.get().strip()
        if not new_name:
            self._show_status("Please enter a new name", "red")
            return
        
        if new_name == self.group.name:
            self._show_status("Name unchanged", "gray")
            return
        
        self.rename_btn.configure(state="disabled")
        try:
            response = self.api_client.update_group_name(self.group.groupId, new_name)
            if response.code == 200:
                self._show_status("Group renamed successfully", "green")
                self.group.name = new_name
                self.title(f"Group: {new_name}")
                if self.on_group_updated:
                    self.on_group_updated()
            else:
                self._show_status(response.message or "Failed to rename", "red")
        except Exception as e:
            self._show_status(f"Error: {e}", "red")
        finally:
            if self.winfo_exists():
                self.rename_btn.configure(state="normal")
    
    def _add_member(self):
        username = self.member_entry.get().strip()
        if not username:
            self._show_status("Please enter a username", "red")
            return
        
        self.add_btn.configure(state="disabled")
        try:
            response = self.api_client.add_member_to_group(self.group.groupId, username)
            if response.code == 200:
                self._show_status(f"Added {username} to group", "green")
                self.member_entry.delete(0, "end")
                self._load_members()
                if self.on_group_updated:
                    self.on_group_updated()
            else:
                self._show_status(response.message or "Failed to add member", "red")
        except Exception as e:
            self._show_status(f"Error: {e}", "red")
        finally:
            if self.winfo_exists():
                self.add_btn.configure(state="normal")
    
    def _leave_group(self):
        if not self._confirm_action("Are you sure you want to leave this group?"):
            return
        
        self.leave_btn.configure(state="disabled")
        try:
            response = self.api_client.leave_group(self.group.groupId)
            if response.code == 200:
                if self.on_group_left:
                    self.on_group_left()
                self.destroy()
            else:
                self._show_status(response.message or "Failed to leave group", "red")
        except Exception as e:
            self._show_status(f"Error: {e}", "red")
        finally:
            if self.winfo_exists():
                self.leave_btn.configure(state="normal")
    
    def _delete_group(self):
        if not self._confirm_action("Are you sure you want to DELETE this group? This cannot be undone."):
            return
        
        self.delete_btn.configure(state="disabled")
        try:
            response = self.api_client.delete_group(self.group.groupId)
            if response.code == 200:
                if self.on_group_left:
                    self.on_group_left()
                self.destroy()
            else:
                self._show_status(response.message or "Failed to delete group", "red")
        except Exception as e:
            self._show_status(f"Error: {e}", "red")
        finally:
            if self.winfo_exists():
                self.delete_btn.configure(state="normal")
    
    def _confirm_action(self, message: str) -> bool:
        """Show a confirmation dialog."""
        dialog = ctk.CTkInputDialog(
            text=f"{message}\n\nType 'yes' to confirm:",
            title="Confirm Action"
        )
        result = dialog.get_input()
        return result and result.lower() == "yes"
