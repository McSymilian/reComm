import customtkinter as ctk
class WelcomeLabelFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.label = ctk.CTkLabel(self, text="Welcome to", font=("Arial", 24))
        self.label.grid(row=0, column=0, pady=20, padx=4)
        self.label2 = ctk.CTkLabel(self, text="reComm", font=("Arial", 24, "bold"))
        self.label2.grid(row=0, column=1, pady=20, padx=4)

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, on_login_success, **kwargs):
        super().__init__(master, **kwargs)
        self.columnconfigure(0, weight=1)

        self.on_login_success = on_login_success

        self.welcome_frame = WelcomeLabelFrame(self)
        self.welcome_frame.grid(row=0, column=0, pady=10, padx=10)

        self.entry_username = ctk.CTkEntry(self, placeholder_text="Username")
        self.entry_username.grid(row=2, column=0, pady=10, padx=10)

        self.entry_password = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.entry_password.grid(row=3, column=0, pady=10, padx=10)

        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.grid(row=4, column=0, pady=5, padx=10)

        self.btn_login = ctk.CTkButton(self, text="Login", command=self.handle_login)
        self.btn_login.grid(row=5, column=0, pady=20, padx=10)
    
    def handle_login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Simple logic (Replace with real auth later)
        if username == "admin" and password == "1234" or 1:
            self.error_label.configure(text="")
            self.on_login_success(username) # Tell the App we are logged in
        else:
            self.error_label.configure(text="Invalid credentials!")