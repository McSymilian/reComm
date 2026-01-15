import customtkinter as ctk

class MessageFrame(ctk.CTkFrame):
    def __init__(self, master, sender, message, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1, )
        self.sender = ctk.CTkLabel(self, text=sender, font=("Arial", 10), pady=0)
        self.sender.grid(column=0, row=0, sticky="e" if sender == "user" else "w", pady=0)

        self.message = ctk.CTkLabel(self, text=message, justify="left", pady=0, wraplength=400)
        self.message.grid(column=0, row=1, sticky="nwes")

class TextInputFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.entry = ctk.CTkEntry(self, placeholder_text="Type your message here...")
        self.entry.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.send_button = ctk.CTkButton(self, text="Send")
        self.send_button.grid(row=0, column=1, padx=5, pady=5)
        self.columnconfigure(0, weight=1)


class MessagesFrame(ctk.CTkScrollableFrame):

    def __init__(self, master, messages, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        for i, (sender, message) in enumerate(messages):
            message_frame = MessageFrame(self, sender, message)
            message_frame.grid(row=i, column=0, sticky="e" if sender == "user" else "w", pady=5, padx=5)
        self.rowconfigure(len(messages), weight=1)




class ConversationFrame(ctk.CTkFrame):
    def __init__(self, master, conversation_name, conversation, **kwargs):
        super().__init__(master, **kwargs)
        self.label = ctk.CTkLabel(self, text=conversation_name, font=("Arial", 30))
        self.label.grid(row=0, column=0, pady=(10, 0))
        self.columnconfigure(0, weight=1)
        self.messages_frame = MessagesFrame(self, messages=conversation)
        self.messages_frame.grid(row=1, column=0, sticky="nsew", pady=10)
        self.rowconfigure(1, weight=1)
        self.text_input_frame = TextInputFrame(self)
        self.text_input_frame.grid(row=2, column=0, sticky="sew", pady=(0, 10))
    
