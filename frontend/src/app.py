import customtkinter as ctk
from .components.navbar import Navbar
from .components.login_frame import LoginFrame
from .components.main_screen import MainScreen
# from .components.input_form import InputForm

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("reComm")
        self.geometry("800x600")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.login_frame = LoginFrame(
            master=self,
            on_login_success=self.show_main_screen
            )
        self.login_frame.grid(row=0, column=0, sticky="nsew")

    def show_main_screen(self, username):
        self.login_frame.destroy()
        self.main_screen = MainScreen(
            master=self,
            username=username
            )
        self.main_screen.grid(row=0, column=0, sticky="nsew")
        # self.input_form = InputForm(self)
        # self.input_form.pack(expand=True, fill="both")