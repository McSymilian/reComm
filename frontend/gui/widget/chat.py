from PyQt6.QtCore import pyqtSignal, Qt, QTimer
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFrame, QHBoxLayout, QLabel, QScrollArea, QLineEdit, QPushButton

from gui.widget.message import MessageWidget


class ChatWidget(QWidget):
    message_sent = pyqtSignal(str)

    def __init__(self, correspondent_name: str, current_username: str, is_group: bool = False, parent=None):
        super().__init__(parent)
        self.send_button = None
        self.message_input = None
        self.messages_layout = None
        self.messages_container = None
        self.scroll_area = None
        self.chat_title = None
        self.correspondent_name = correspondent_name
        self.current_username = current_username
        self.is_group = is_group
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        header = QFrame()
        header.setFrameShape(QFrame.Shape.StyledPanel)
        header.setMaximumHeight(40)
        header_layout = QHBoxLayout(header)

        if self.is_group:
            self.chat_title = QLabel(f"Grupa: {self.correspondent_name}")
        else:
            self.chat_title = QLabel(f"Czat z: {self.correspondent_name}")
        self.chat_title.setStyleSheet("font-size: 14px; font-weight: bold;")
        header_layout.addWidget(self.chat_title)
        header_layout.addStretch()

        layout.addWidget(header)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.messages_container = QWidget()
        self.messages_layout = QVBoxLayout(self.messages_container)
        self.messages_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.messages_layout.setSpacing(5)

        self.scroll_area.setWidget(self.messages_container)
        layout.addWidget(self.scroll_area)

        input_container = QWidget()
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(5, 5, 5, 5)

        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Wpisz wiadomość...")
        self.message_input.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.message_input)

        self.send_button = QPushButton("Wyślij")
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)

        layout.addWidget(input_container)

    def add_message(self, author: str, content: str, is_own: bool):
        message_widget = MessageWidget(author, content, is_own)
        self.messages_layout.addWidget(message_widget)

        QTimer.singleShot(100, self.scroll_to_bottom)

    def scroll_to_bottom(self):
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def clear_messages(self):
        while self.messages_layout.count():
            item = self.messages_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def send_message(self):
        message = self.message_input.text().strip()
        if message:
            self.message_sent.emit(message)
            self.message_input.clear()