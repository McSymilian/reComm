from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QListWidget, QListWidgetItem, QGroupBox, QMessageBox
)


class GroupSettingsDialog(QDialog):

    def __init__(self, group_id: str, group_name: str, members: list,
                 current_username: str, owner_username: str, api_service, parent=None):
        super().__init__(parent)
        self.group_id = group_id
        self.group_name = group_name
        self.members = members or []
        self.current_username = current_username
        self.owner_username = owner_username
        self.api_service = api_service
        self.is_owner = (current_username == owner_username)

        self.setWindowTitle(f"Ustawienia grupy: {group_name}")
        self.setMinimumWidth(400)
        self.setMinimumHeight(450)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Sekcja zmiany nazwy grupy
        name_group = QGroupBox("Nazwa grupy")
        name_layout = QHBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setText(self.group_name)
        name_layout.addWidget(self.name_input)

        self.change_name_button = QPushButton("Zmień")
        self.change_name_button.clicked.connect(self.on_change_name)
        name_layout.addWidget(self.change_name_button)

        name_group.setLayout(name_layout)
        layout.addWidget(name_group)

        # Sekcja członków grupy
        members_group = QGroupBox("Członkowie grupy")
        members_layout = QVBoxLayout()

        self.members_list = QListWidget()
        self.load_members()
        members_layout.addWidget(self.members_list)

        # Dodawanie nowego członka
        add_member_layout = QHBoxLayout()
        self.new_member_input = QLineEdit()
        self.new_member_input.setPlaceholderText("Nazwa użytkownika")
        add_member_layout.addWidget(self.new_member_input)

        self.add_member_button = QPushButton("Dodaj członka")
        self.add_member_button.clicked.connect(self.on_add_member)
        add_member_layout.addWidget(self.add_member_button)

        members_layout.addLayout(add_member_layout)
        members_group.setLayout(members_layout)
        layout.addWidget(members_group)

        # Przyciski akcji
        actions_layout = QHBoxLayout()

        if self.is_owner:
            # Właściciel może usunąć grupę
            self.delete_button = QPushButton("🗑 Usuń grupę")
            self.delete_button.setStyleSheet("""
                QPushButton {
                    background-color: #f44336;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    font-size: 13px;
                    font-weight: bold;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #da190b;
                }
            """)
            self.delete_button.clicked.connect(self.on_delete_group)
            actions_layout.addWidget(self.delete_button)
        else:
            # Pozostali mogą opuścić grupę
            self.leave_button = QPushButton("🚪 Opuść grupę")
            self.leave_button.setStyleSheet("""
                QPushButton {
                    background-color: #ff9800;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    font-size: 13px;
                    font-weight: bold;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #f57c00;
                }
            """)
            self.leave_button.clicked.connect(self.on_leave_group)
            actions_layout.addWidget(self.leave_button)

        actions_layout.addStretch()

        self.close_button = QPushButton("Zamknij")
        self.close_button.clicked.connect(self.accept)
        actions_layout.addWidget(self.close_button)

        layout.addLayout(actions_layout)

    def load_members(self):
        """Ładuje listę członków grupy."""
        self.members_list.clear()
        for member in self.members:
            if isinstance(member, dict):
                username = member.get('username', str(member))
            else:
                username = str(member)

            # Oznacz właściciela
            if username == self.owner_username:
                item = QListWidgetItem(f"👑 {username} (właściciel)")
            else:
                item = QListWidgetItem(f"👤 {username}")

            self.members_list.addItem(item)

    def on_change_name(self):
        """Zmienia nazwę grupy."""
        new_name = self.name_input.text().strip()
        if not new_name:
            QMessageBox.warning(self, "Błąd", "Wprowadź nową nazwę grupy.")
            return

        if new_name == self.group_name:
            return

        try:
            success = self.api_service.change_group_name(self.group_id, new_name)
            if success:
                self.group_name = new_name
                self.setWindowTitle(f"Ustawienia grupy: {new_name}")
                QMessageBox.information(self, "Sukces", f"Zmieniono nazwę grupy na '{new_name}'.")
            else:
                QMessageBox.warning(self, "Błąd", "Nie udało się zmienić nazwy grupy.")
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd: {str(e)}")

    def on_add_member(self):
        """Dodaje nowego członka do grupy."""
        username = self.new_member_input.text().strip()
        if not username:
            QMessageBox.warning(self, "Błąd", "Wprowadź nazwę użytkownika.")
            return

        try:
            success = self.api_service.add_member_to_group(self.group_id, username)
            if success:
                self.new_member_input.clear()
                # Odśwież listę członków
                self.members = self.api_service.get_group_members(self.group_id) or []
                self.load_members()
                QMessageBox.information(self, "Sukces", f"Dodano {username} do grupy.")
            else:
                QMessageBox.warning(self, "Błąd", f"Nie udało się dodać {username} do grupy.")
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd: {str(e)}")

    def on_leave_group(self):
        """Opuszcza grupę."""
        reply = QMessageBox.question(
            self,
            "Potwierdź wyjście",
            f"Czy na pewno chcesz opuścić grupę '{self.group_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                success = self.api_service.leave_group(self.group_id)
                if success:
                    QMessageBox.information(self, "Sukces", f"Opuściłeś grupę '{self.group_name}'.")
                    self.reject()  # Zamknij dialog
                else:
                    QMessageBox.warning(self, "Błąd", "Nie udało się opuścić grupy.")
            except Exception as e:
                QMessageBox.critical(self, "Błąd", f"Wystąpił błąd: {str(e)}")

    def on_delete_group(self):
        """Usuwa grupę (tylko dla właściciela)."""
        reply = QMessageBox.question(
            self,
            "Potwierdź usunięcie",
            f"Czy na pewno chcesz USUNĄĆ grupę '{self.group_name}'?\n\nTa operacja jest nieodwracalna!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                success = self.api_service.delete_group(self.group_id)
                if success:
                    QMessageBox.information(self, "Sukces", f"Usunięto grupę '{self.group_name}'.")
                    self.reject()  # Zamknij dialog
                else:
                    QMessageBox.warning(self, "Błąd", "Nie udało się usunąć grupy.")
            except Exception as e:
                QMessageBox.critical(self, "Błąd", f"Wystąpił błąd: {str(e)}")
