import customtkinter as ctk
from .components.login_frame import LoginFrame
from .components.main_screen import MainScreen
from .components.top_navbar import TopNavbar
from .utils.api_client import APIClient
from .utils.data_store import DataStore


class App(ctk.CTk):
    def __init__(self, host: str = "192.168.100.44", port: int = 8080):
        super().__init__()
        
        self.title("reComm")
        self.geometry("1000x700")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.api_client = APIClient(host=host, 
        port=port)
        self.data_store = None
        
        self.top_navbar = None
        self.main_screen = None

        self.login_frame = LoginFrame(
            master=self,
            api_client=self.api_client,
            on_login_success=self.show_main_screen
            )
        self.login_frame.grid(row=0, column=0, sticky="nsew")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def show_main_screen(self, username):
        self.login_frame.destroy()
        
        self.data_store = DataStore(self.api_client)
        self.data_store.initialize()
        
        self.top_navbar = TopNavbar(
            master=self,
            username=username,
            on_logout=self.logout
        )
        self.top_navbar.grid(row=0, column=0, sticky="ew")
        
        self.main_screen = MainScreen(
            master=self,
            username=username,
            api_client=self.api_client,
            data_store=self.data_store
            )
        self.main_screen.grid(row=1, column=0, sticky="nsew")

    def logout(self):
        if self.main_screen:
            self.main_screen.destroy()
            self.main_screen = None
        if self.top_navbar:
            self.top_navbar.destroy()
            self.top_navbar = None
        
        if self.data_store:
            self.data_store.reset()
            self.data_store = None
        
        self.api_client.clear_token()
        
        self.login_frame = LoginFrame(
            master=self,
            api_client=self.api_client,
            on_login_success=self.show_main_screen
        )
        self.login_frame.grid(row=0, column=0, sticky="nsew")
    
    def on_closing(self):
        if self.data_store:
            self.data_store.reset()
        if self.api_client:
            self.api_client.close()
        self.destroy()