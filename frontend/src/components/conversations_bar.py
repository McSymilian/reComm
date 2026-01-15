import customtkinter as ctk

class ConversationsBar(ctk.CTkFrame):
    def __init__(self, master, conversations, **kwargs):
        super().__init__(master, width=250, corner_radius=0, **kwargs)

        for i, conversation in enumerate(conversations):
            btn = ctk.CTkButton(self, text=conversation)
            btn.grid(row=i, pady=5, padx=10)