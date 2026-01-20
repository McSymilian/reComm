from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


class MessageWidget(QWidget):
    def __init__(self, author: str, content: str, is_own: bool, parent=None):
        super().__init__(parent)
        self.author = author
        self.content = content
        self.is_own = is_own
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)

        message_container = QWidget()
        message_layout = QVBoxLayout(message_container)
        message_layout.setContentsMargins(10, 5, 10, 5)

        author_label = QLabel(self.author)
        author_label.setStyleSheet("font-size: 10px; color: #363430; font-weight: bold;")
        message_layout.addWidget(author_label)

        content_label = QLabel(self.content)
        content_label.setWordWrap(True)
        content_label.setStyleSheet("font-size: 13px;")
        message_layout.addWidget(content_label)

        if self.is_own:
            message_container.setStyleSheet("""
                QWidget {
                    background-color: #DCF8C6;
                    border-radius: 10px;
                    color: black;
                }
            """)
            layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        else:
            message_container.setStyleSheet("""
                QWidget {
                    background-color: #E8E8E8;
                    border-radius: 10px;
                    color: black;
                }
            """)
            layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        layout.addWidget(message_container)
