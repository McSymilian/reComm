import logging
import threading

from PyQt6.QtCore import Qt, QTimer, QSize, pyqtSignal, QObject
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QGroupBox, QSplitter, QFrame,
    QPushButton, QDialog, QMessageBox
)

from gui.dialog.add_friend import AddFriendDialog
from gui.dialog.create_group import CreateGroupDialog
from gui.dialog.friend_request import FriendRequestWidget
from gui.dialog.group_settings import GroupSettingsDialog
from gui.widget.chat import ChatWidget
from gui.widget.connection_indicator import ConnectionIndicator
from gui.widget.group_item import GroupItemWidget
from tools.api_service import ApiService

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class NotificationWorker(QObject):

    new_message_received = pyqtSignal(dict)
    friend_request_received = pyqtSignal(dict)

    def __init__(self, notification_queue):
        super().__init__()
        self.notification_queue = notification_queue
        self.running = True

    def run(self):
        while self.running:
            try:
                notification = self.notification_queue.get(timeout=1.0)

                if notification.get('type') == 'NEW_PRIVATE_MESSAGE':
                    self.new_message_received.emit(notification)
                elif notification.get('type') == 'FRIEND_REQUEST':
                    self.friend_request_received.emit(notification)

            except Exception:
                pass

    def stop(self):
        self.running = False


class MainWindow(QMainWindow):
    def __init__(self, api_service: ApiService, user: dict[str, str]):
        super().__init__()
        self.placeholder_label = None
        self.create_group_button = None
        self.add_friend_button = None
        self.groups_list = None
        self.friends_list = None
        self.connection_indicator = None
        self.username_label = None
        self.splitter = None
        self.main_content = None
        self.main_content_layout = None
        self.chat_widget = None
        self.current_chat_friend = None
        self.current_chat_group_id = None
        self.current_chat_group_name = None
        self.cached_friends = []
        self.cached_pending_requests = []
        self.cached_groups = []
        self.api_service = api_service
        self.username = user['username']
        self.init_ui()
        self.load_data()

        self.connection_timer = QTimer()
        self.connection_timer.timeout.connect(self.check_connection)
        self.connection_timer.start(5000)

        self.friends_timer = QTimer()
        self.friends_timer.timeout.connect(self.load_friends)
        self.friends_timer.start(1000)

        self.groups_timer = QTimer()
        self.groups_timer.timeout.connect(self.load_groups)
        self.groups_timer.start(1000)

        self.notification_worker = NotificationWorker(self.api_service.notification_queue)
        self.notification_worker.new_message_received.connect(self.on_new_message_received)
        self.notification_worker.friend_request_received.connect(self.on_friend_request_received)
        self.notification_thread = threading.Thread(target=self.notification_worker.run, daemon=True)
        self.notification_thread.start()

    def init_ui(self):
        self.setWindowTitle("reComm")
        self.setMinimumSize(800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        top_bar = QFrame()
        top_bar.setFrameShape(QFrame.Shape.StyledPanel)
        top_bar.setMaximumHeight(50)
        top_bar_layout = QHBoxLayout(top_bar)

        self.username_label = QLabel(self.username)
        self.username_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        top_bar_layout.addWidget(self.username_label)

        self.connection_indicator = ConnectionIndicator()
        self.connection_indicator.set_connected(True)
        top_bar_layout.addWidget(self.connection_indicator)

        top_bar_layout.addStretch()

        main_layout.addWidget(top_bar)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        left_panel = QWidget()
        left_panel.setMaximumWidth(300)
        left_panel.setMinimumWidth(200)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)

        friends_group = QGroupBox("Przyjaciele")
        friends_layout = QVBoxLayout()
        self.friends_list = QListWidget()
        self.friends_list.setMinimumHeight(150)
        self.friends_list.itemClicked.connect(self.on_friend_clicked)
        friends_layout.addWidget(self.friends_list)

        self.add_friend_button = QPushButton("Dodaj przyjaciela")
        self.add_friend_button.clicked.connect(self.show_add_friend_dialog)
        friends_layout.addWidget(self.add_friend_button)

        friends_group.setLayout(friends_layout)
        left_layout.addWidget(friends_group)

        groups_group = QGroupBox("Grupy")
        groups_layout = QVBoxLayout()
        self.groups_list = QListWidget()
        self.groups_list.setMinimumHeight(150)
        self.groups_list.itemClicked.connect(self.on_group_clicked)
        groups_layout.addWidget(self.groups_list)

        self.create_group_button = QPushButton("Stwórz grupę")
        self.create_group_button.clicked.connect(self.show_create_group_dialog)
        groups_layout.addWidget(self.create_group_button)

        groups_group.setLayout(groups_layout)
        left_layout.addWidget(groups_group)

        splitter.addWidget(left_panel)

        self.main_content = QFrame()
        self.main_content.setFrameShape(QFrame.Shape.StyledPanel)
        self.main_content_layout = QVBoxLayout(self.main_content)

        self.placeholder_label = QLabel("Wybierz rozmowę z listy po lewej stronie")
        self.placeholder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.placeholder_label.setStyleSheet("color: gray; font-size: 14px;")
        self.main_content_layout.addWidget(self.placeholder_label)

        splitter.addWidget(self.main_content)

        splitter.setSizes([250, 550])
        self.splitter = splitter

        main_layout.addWidget(splitter)

    def load_data(self):
        self.load_friends()
        self.load_groups()

    def load_friends(self):
        try:
            pending_requests = self.api_service.get_pending_friend_requests() or []
            friends = self.api_service.get_all_friends() or []

            # Normalizuj dane do porównania
            new_pending = []
            for request in pending_requests:
                if isinstance(request, dict):
                    requester = request.get('from', request.get('requester', 'null'))
                    if (not requester) and self.username == request:
                        requester = request.get('addressee', 'null')
                else:
                    requester = str(request)
                if requester:
                    new_pending.append(requester)

            new_friends = [str(friend) for friend in friends]

            # Sprawdź czy listy się zmieniły
            if new_pending == self.cached_pending_requests and new_friends == self.cached_friends:
                return  # Brak zmian, nie odświeżaj UI

            # Zaktualizuj cache
            self.cached_pending_requests = new_pending
            self.cached_friends = new_friends

            # Odśwież UI
            logger.info(f"Refreshing friend list - changes detected")
            self.friends_list.clear()

            for requester in new_pending:
                item = QListWidgetItem()
                item.setSizeHint(QSize(0, 30))
                self.friends_list.addItem(item)

                request_widget = FriendRequestWidget(requester)
                request_widget.accepted.connect(self.on_accept_friend_request)
                request_widget.rejected.connect(self.on_reject_friend_request)
                self.friends_list.setItemWidget(item, request_widget)

            for friend_name in new_friends:
                item = QListWidgetItem(friend_name)
                self.friends_list.addItem(item)

        except Exception as e:
            logger.warning(f"Błąd podczas pobierania przyjaciół: {e}")

    def load_groups(self):
        try:
            groups = self.api_service.get_all_users_groups() or []

            # Normalizuj dane do porównania
            new_groups = []
            for group in groups:
                if isinstance(group, dict):
                    group_id = group.get('id', group.get('groupId', ''))
                    group_name = group.get('name', group.get('groupName', str(group)))
                else:
                    group_id = str(group)
                    group_name = str(group)
                new_groups.append((group_id, group_name))

            # Sprawdź czy lista się zmieniła
            if new_groups == self.cached_groups:
                return  # Brak zmian, nie odświeżaj UI

            # Zaktualizuj cache
            self.cached_groups = new_groups

            # Odśwież UI
            logger.info(f"Refreshing groups list - changes detected")
            self.groups_list.clear()

            for group_id, group_name in new_groups:
                item = QListWidgetItem()
                item.setSizeHint(QSize(0, 30))
                self.groups_list.addItem(item)

                group_widget = GroupItemWidget(group_id, group_name)
                group_widget.settings_clicked.connect(self.on_group_settings)
                self.groups_list.setItemWidget(item, group_widget)

        except Exception as e:
            logger.warning(f"Błąd podczas pobierania grup: {e}")

    def check_connection(self):
        try:
            is_connected = self.api_service.tcp_client.is_connected
            self.connection_indicator.set_connected(is_connected)
            logger.debug(f"Connected: {is_connected}")
        except Exception:
            logger.warning("Connection error")
            self.connection_indicator.set_connected(False)

    def show_add_friend_dialog(self):
        dialog = AddFriendDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            username = dialog.get_username()
            if username:
                try:
                    success = self.api_service.send_friend_request(username)
                    if success:
                        QMessageBox.information(self, "Sukces", f"Wysłano zaproszenie do {username}!")
                    else:
                        QMessageBox.warning(self, "Błąd", f"Nie udało się wysłać zaproszenia do {username}.")
                except Exception as e:
                    QMessageBox.critical(self, "Błąd", f"Wystąpił błąd: {str(e)}")
            else:
                QMessageBox.warning(self, "Błąd", "Wprowadź nazwę użytkownika.")

    def show_create_group_dialog(self):
        dialog = CreateGroupDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            group_name = dialog.get_group_name()
            if group_name:
                try:
                    group_id = self.api_service.create_group(group_name)
                    if group_id:
                        QMessageBox.information(self, "Sukces", f"Utworzono grupę '{group_name}'!")
                        self.load_groups()
                    else:
                        QMessageBox.warning(self, "Błąd", f"Nie udało się utworzyć grupy '{group_name}'.")
                except Exception as e:
                    QMessageBox.critical(self, "Błąd", f"Wystąpił błąd: {str(e)}")
            else:
                QMessageBox.warning(self, "Błąd", "Wprowadź nazwę grupy.")

    def on_group_settings(self, group_id: str, group_name: str):
        """Otwiera okno ustawień grupy."""
        try:
            # Pobierz szczegóły grupy
            group_details = self.api_service.get_group_details(group_id)
            members = self.api_service.get_group_members(group_id) or []

            # Pobierz właściciela grupy
            owner_username = ""
            if group_details and isinstance(group_details, dict):
                owner_username = group_details.get('owner', group_details.get('ownerUsername', ''))

            dialog = GroupSettingsDialog(
                group_id=group_id,
                group_name=group_name,
                members=members,
                current_username=self.username,
                owner_username=owner_username,
                api_service=self.api_service,
                parent=self
            )
            dialog.exec()

            # Odśwież listę grup po zamknięciu dialogu
            self.load_groups()

        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się otworzyć ustawień grupy: {str(e)}")

    def on_friend_clicked(self, item: QListWidgetItem):
        friend_name = item.text()
        self.current_chat_friend = friend_name
        self.current_chat_group_id = None
        self.current_chat_group_name = None

        while self.main_content_layout.count():
            child = self.main_content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.chat_widget = ChatWidget(friend_name, self.username, is_group=False)
        self.chat_widget.message_sent.connect(self.on_send_message)
        self.main_content_layout.addWidget(self.chat_widget)

        self.load_chat_messages(friend_name)

    def load_chat_messages(self, friend_name: str):
        try:
            messages = self.api_service.get_private_messages(friend_name)
            if messages and self.chat_widget:
                sorted_messages = sorted(messages, key=lambda m: m.get('sentAt', 0) if isinstance(m, dict) else 0)

                for msg in sorted_messages:
                    if isinstance(msg, dict):
                        author = msg.get('senderName', 'null')
                        content = msg.get('content', 'null')
                    else:
                        author = ''
                        content = str(msg)

                    is_own = (author == self.username)
                    self.chat_widget.add_message(author, content, is_own)
        except Exception as e:
            logger.warning(f"Błąd podczas ładowania wiadomości: {e}")

    def on_send_message(self, message: str):
        if self.current_chat_friend and message:
            try:
                message_id = self.api_service.send_message_to_user(self.current_chat_friend, message)
                if message_id:
                    if self.chat_widget:
                        self.chat_widget.add_message(self.username, message, True)
                else:
                    QMessageBox.warning(self, "Błąd", "Nie udało się wysłać wiadomości.")
            except Exception as e:
                QMessageBox.critical(self, "Błąd", f"Wystąpił błąd: {str(e)}")
        elif self.current_chat_group_id and message:
            try:
                message_id = self.api_service.send_message_to_group(self.current_chat_group_id, message)
                if message_id:
                    if self.chat_widget:
                        self.chat_widget.add_message(self.username, message, True)
                else:
                    QMessageBox.warning(self, "Błąd", "Nie udało się wysłać wiadomości do grupy.")
            except Exception as e:
                QMessageBox.critical(self, "Błąd", f"Wystąpił błąd: {str(e)}")

    def on_group_clicked(self, item: QListWidgetItem):
        widget = self.groups_list.itemWidget(item)
        if not isinstance(widget, GroupItemWidget):
            return

        group_id = widget.group_id
        group_name = widget.group_name

        self.current_chat_group_id = group_id
        self.current_chat_group_name = group_name
        self.current_chat_friend = None

        while self.main_content_layout.count():
            child = self.main_content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.chat_widget = ChatWidget(group_name, self.username, is_group=True)
        self.chat_widget.message_sent.connect(self.on_send_message)
        self.main_content_layout.addWidget(self.chat_widget)

        self.load_group_chat_messages(group_id)

    def load_group_chat_messages(self, group_id: str):
        """Ładuje historię wiadomości z grupy."""
        try:
            messages = self.api_service.get_group_messages(group_id)
            if messages and self.chat_widget:
                sorted_messages = sorted(messages, key=lambda m: m.get('sentAt', 0) if isinstance(m, dict) else 0)

                for msg in sorted_messages:
                    if isinstance(msg, dict):
                        author = msg.get('senderName', msg.get('sender', ''))
                        content = msg.get('content', msg.get('message', ''))
                    else:
                        author = ''
                        content = str(msg)

                    is_own = (author == self.username)
                    self.chat_widget.add_message(author, content, is_own)
        except Exception as e:
            logger.warning(f"Błąd podczas ładowania wiadomości grupowych: {e}")

    def on_new_message_received(self, notification: dict):
        """Obsługuje nową wiadomość otrzymaną z wątku powiadomień."""
        try:
            sender = notification.get('senderName', notification.get('sender', ''))
            content = notification.get('content', notification.get('message', ''))

            # Sprawdź czy to wiadomość od aktualnie wybranego przyjaciela
            if self.current_chat_friend and sender == self.current_chat_friend:
                if self.chat_widget:
                    is_own = (sender == self.username)
                    self.chat_widget.add_message(sender, content, is_own)

            logger.debug(f"Otrzymano nową wiadomość od {sender}: {content}")
        except Exception as e:
            logger.warning(f"Błąd podczas obsługi nowej wiadomości: {e}")

    def on_friend_request_received(self, notification: dict):
        try:
            requester = notification.get('from')

            if requester:
                for i in range(self.friends_list.count()):
                    item = self.friends_list.item(i)
                    widget = self.friends_list.itemWidget(item)
                    if isinstance(widget, FriendRequestWidget) and widget.requester_username == requester:
                        return

                item = QListWidgetItem()
                item.setSizeHint(QSize(0, 30))
                self.friends_list.insertItem(0, item)

                request_widget = FriendRequestWidget(requester)
                request_widget.accepted.connect(self.on_accept_friend_request)
                request_widget.rejected.connect(self.on_reject_friend_request)
                self.friends_list.setItemWidget(item, request_widget)

                logger.info(f"Otrzymano zaproszenie do znajomych od {requester}")
        except Exception as e:
            logger.warning(f"Błąd podczas obsługi zaproszenia do znajomych: {e}")

    def on_accept_friend_request(self, requester_username: str):
        """Akceptuje zaproszenie do znajomych."""
        try:
            success = self.api_service.accept_friend_request(requester_username)
            if success:
                logger.info(f"Zaakceptowano zaproszenie od {requester_username}")
                self.load_friends()  # Odśwież listę przyjaciół
            else:
                QMessageBox.warning(self, "Błąd", f"Nie udało się zaakceptować zaproszenia od {requester_username}.")
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd: {str(e)}")

    def on_reject_friend_request(self, requester_username: str):
        """Odrzuca zaproszenie do znajomych."""
        try:
            success = self.api_service.reject_friend_request(requester_username)
            if success:
                logger.info(f"Odrzucono zaproszenie od {requester_username}")
                self.load_friends()  # Odśwież listę przyjaciół
            else:
                QMessageBox.warning(self, "Błąd", f"Nie udało się odrzucić zaproszenia od {requester_username}.")
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd: {str(e)}")

    def closeEvent(self, event):
        self.connection_timer.stop()
        self.friends_timer.stop()
        self.groups_timer.stop()

        # Zatrzymaj wątek powiadomień
        if hasattr(self, 'notification_worker'):
            self.notification_worker.stop()

        try:
            self.api_service.tcp_client.disconnect()
        except Exception:
            pass
        event.accept()
