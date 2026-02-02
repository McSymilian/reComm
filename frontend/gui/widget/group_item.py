from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy, QPushButton


class GroupItemWidget(QWidget):
    settings_clicked = pyqtSignal(str, str)  # group_id, group_name

    def __init__(self, group_id: str, group_name: str, parent=None):
        super().__init__(parent)
        self.settings_button = None
        self.name_label = None
        self.group_id = group_id
        self.group_name = group_name
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 2, 5, 2)

        self.name_label = QLabel(self.group_name)
        self.name_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        layout.addWidget(self.name_label)

        self.settings_button = QPushButton("☰")
        self.settings_button.setFixedSize(20, 20)
        self.settings_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #888;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                color: #1976D2;
            }
        """)
        self.settings_button.setToolTip("Ustawienia grupy")
        self.settings_button.clicked.connect(self.on_settings_clicked)
        layout.addWidget(self.settings_button)

    def on_settings_clicked(self):
        self.settings_clicked.emit(self.group_id, self.group_name)
