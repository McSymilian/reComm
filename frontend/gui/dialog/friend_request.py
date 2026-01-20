from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QPushButton, QSizePolicy
)
from PyQt6.QtCore import pyqtSignal


class FriendRequestWidget(QWidget):
    """Widget reprezentujący zaproszenie do znajomych z przyciskami accept/deny."""

    accepted = pyqtSignal(str)  # Sygnał emitowany po akceptacji (username)
    rejected = pyqtSignal(str)  # Sygnał emitowany po odrzuceniu (username)

    def __init__(self, requester_username: str, parent=None):
        super().__init__(parent)
        self.requester_username = requester_username
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 2, 5, 2)

        # Nazwa użytkownika z ikoną zaproszenia
        self.name_label = QLabel(f"📩 {self.requester_username}")
        self.name_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.name_label.setStyleSheet("font-weight: bold; color: #1976D2;")
        layout.addWidget(self.name_label)

        # Przycisk Accept (zielony)
        self.accept_button = QPushButton("✓")
        self.accept_button.setFixedSize(24, 24)
        self.accept_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 12px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.accept_button.setToolTip("Akceptuj zaproszenie")
        self.accept_button.clicked.connect(self.on_accept)
        layout.addWidget(self.accept_button)

        # Przycisk Deny (czerwony)
        self.deny_button = QPushButton("✕")
        self.deny_button.setFixedSize(24, 24)
        self.deny_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 12px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        self.deny_button.setToolTip("Odrzuć zaproszenie")
        self.deny_button.clicked.connect(self.on_deny)
        layout.addWidget(self.deny_button)

    def on_accept(self):
        self.accepted.emit(self.requester_username)

    def on_deny(self):
        self.rejected.emit(self.requester_username)
