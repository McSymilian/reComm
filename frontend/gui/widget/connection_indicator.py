from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QBrush
from PyQt6.QtWidgets import QWidget


class ConnectionIndicator(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.connected = False
        self.setFixedSize(16, 16)

    def set_connected(self, connected: bool):
        self.connected = connected
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self.connected:
            color = QColor(0, 200, 0)
        else:
            color = QColor(200, 0, 0)

        painter.setBrush(QBrush(color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(2, 2, 12, 12)
