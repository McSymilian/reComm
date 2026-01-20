import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QGroupBox, QMessageBox
)

from tools.api_service import ApiService
from gui.main_window import MainWindow


class LoginWindow(QWidget):
    def __init__(self, ):
        super().__init__()
        self.user = None
        self.register_button = None
        self.login_button = None
        self.username_input = None
        self.password_input = None
        self.connection_status_label = None
        self.connect_button = None
        self.port_input = None
        self.ip_input = None
        self.api_service = None
        self.main_window = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("reComm")
        self.setMinimumWidth(400)

        main_layout = QVBoxLayout()

        connection_group = QGroupBox("Połączenie z serwerem")
        connection_layout = QVBoxLayout()

        ip_layout = QHBoxLayout()
        ip_label = QLabel("Adres IP:")
        ip_label.setFixedWidth(100)
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("np. 127.0.0.1")
        ip_layout.addWidget(ip_label)
        ip_layout.addWidget(self.ip_input)
        connection_layout.addLayout(ip_layout)

        # Port
        port_layout = QHBoxLayout()
        port_label = QLabel("Port:")
        port_label.setFixedWidth(100)
        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("np. 8080")
        port_layout.addWidget(port_label)
        port_layout.addWidget(self.port_input)
        connection_layout.addLayout(port_layout)

        connect_status_layout = QHBoxLayout()
        self.connect_button = QPushButton("Połącz")
        self.connect_button.clicked.connect(self.on_connect)
        self.connection_status_label = QLabel("Status: Niepołączony")
        self.connection_status_label.setStyleSheet("color: red; font-weight: bold;")
        connect_status_layout.addWidget(self.connect_button)
        connect_status_layout.addWidget(self.connection_status_label)
        connection_layout.addLayout(connect_status_layout)

        connection_group.setLayout(connection_layout)
        main_layout.addWidget(connection_group)

        login_group = QGroupBox("Dane logowania")
        login_layout = QVBoxLayout()

        username_layout = QHBoxLayout()
        username_label = QLabel("Nazwa użytkownika:")
        username_label.setFixedWidth(130)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Wprowadź nazwę użytkownika")
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        login_layout.addLayout(username_layout)

        password_layout = QHBoxLayout()
        password_label = QLabel("Hasło:")
        password_label.setFixedWidth(130)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Wprowadź hasło")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        login_layout.addLayout(password_layout)

        login_group.setLayout(login_layout)
        main_layout.addWidget(login_group)

        buttons_layout = QHBoxLayout()
        self.login_button = QPushButton("Zaloguj")
        self.login_button.clicked.connect(self.on_login)
        self.login_button.setEnabled(False)

        self.register_button = QPushButton("Zarejestruj")
        self.register_button.clicked.connect(self.on_register)
        self.register_button.setEnabled(False)

        buttons_layout.addWidget(self.login_button)
        buttons_layout.addWidget(self.register_button)
        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

    def on_connect(self):
        ip = self.ip_input.text().strip()
        port_text = self.port_input.text().strip()

        if not ip:
            QMessageBox.warning(self, "Błąd", "Wprowadź adres IP serwera.")
            return

        if not port_text:
            QMessageBox.warning(self, "Błąd", "Wprowadź numer portu.")
            return

        try:
            port = int(port_text)
        except ValueError:
            QMessageBox.warning(self, "Błąd", "Port musi być liczbą.")
            return

        try:
            self.api_service = ApiService(host=ip, port=port)
            self.connection_status_label.setText("Status: Połączono")
            self.connection_status_label.setStyleSheet("color: green; font-weight: bold;")
            self.connect_button.setEnabled(False)
            self.ip_input.setEnabled(False)
            self.port_input.setEnabled(False)
            self.login_button.setEnabled(True)
            self.register_button.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "Błąd połączenia", f"Nie udało się połączyć z serwerem:\n{str(e)}")
            self.connection_status_label.setText("Status: Błąd połączenia")
            self.connection_status_label.setStyleSheet("color: red; font-weight: bold;")

    def on_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()

        if not username:
            QMessageBox.warning(self, "Błąd", "Wprowadź nazwę użytkownika.")
            return

        if not password:
            QMessageBox.warning(self, "Błąd", "Wprowadź hasło.")
            return

        try:
            success = self.api_service.login(username, password)
            if success:
                self.user = {
                    "username": username
                }
                self.open_main_window()
            else:
                QMessageBox.warning(self, "Błąd logowania", "Nieprawidłowa nazwa użytkownika lub hasło.")
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas logowania:\n{str(e)}")

    def on_register(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()

        if not username:
            QMessageBox.warning(self, "Błąd", "Wprowadź nazwę użytkownika.")
            return

        if not password:
            QMessageBox.warning(self, "Błąd", "Wprowadź hasło.")
            return

        try:
            success = self.api_service.register(username, password)
            if success:
                self.user = {
                    "username": username
                }
                self.open_main_window()
            else:
                QMessageBox.warning(self, "Błąd rejestracji", "Nie udało się zarejestrować. Użytkownik może już istnieć.")
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas rejestracji:\n{str(e)}")

    def open_main_window(self):
        self.main_window = MainWindow(self.api_service, self.user)
        self.main_window.show()
        self.close()


def main():
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
