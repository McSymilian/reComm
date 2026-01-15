import customtkinter as ctk

class Navbar(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, width=200, corner_radius=0, **kwargs)
        
        self.label = ctk.CTkLabel(self, text="Menu", font=("Arial", 20))
        self.label.pack(pady=20, padx=10)

        self.btn_home = ctk.CTkButton(self, text="Home")
        self.btn_home.pack(pady=10, padx=10)
        
        self.btn_settings = ctk.CTkButton(self, text="Settings")
        self.btn_settings.pack(pady=10, padx=10)