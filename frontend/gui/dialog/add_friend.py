from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton


class AddFriendDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.cancel_button = None
        self.username_input = None
        self.send_button = None
        self.setWindowTitle("Dodaj przyjaciela")
        self.setMinimumWidth(300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        label = QLabel("Nazwa użytkownika:")
        layout.addWidget(label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Wpisz nazwę użytkownika")
        layout.addWidget(self.username_input)

        buttons_layout = QHBoxLayout()

        self.send_button = QPushButton("Wyślij")
        self.send_button.clicked.connect(self.accept)
        buttons_layout.addWidget(self.send_button)

        self.cancel_button = QPushButton("Anuluj")
        self.cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(self.cancel_button)

        layout.addLayout(buttons_layout)

    def get_username(self) -> str:
        return self.username_input.text().strip()