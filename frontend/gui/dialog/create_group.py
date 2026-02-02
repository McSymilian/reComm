from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton


class CreateGroupDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.cancel_button = None
        self.create_button = None
        self.group_name_input = None
        self.setWindowTitle("Stwórz grupę")
        self.setMinimumWidth(300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        label = QLabel("Nazwa grupy:")
        layout.addWidget(label)

        self.group_name_input = QLineEdit()
        self.group_name_input.setPlaceholderText("Wpisz nazwę grupy")
        layout.addWidget(self.group_name_input)

        buttons_layout = QHBoxLayout()

        self.create_button = QPushButton("Stwórz")
        self.create_button.clicked.connect(self.accept)
        buttons_layout.addWidget(self.create_button)

        self.cancel_button = QPushButton("Anuluj")
        self.cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(self.cancel_button)

        layout.addLayout(buttons_layout)

    def get_group_name(self) -> str:
        return self.group_name_input.text().strip()
