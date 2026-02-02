#!/usr/bin/env python3

import socket
import threading
import time
import logging
from typing import Callable, Optional
from queue import Queue
from enum import Enum

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ConnectionState(Enum):
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    RECONNECTING = "reconnecting"


class TCPClient:
    def __init__(
        self,
        host: str,
        port: int,
        reconnect_delay: float = 2.0,
        max_reconnect_delay: float = 30.0,
        heartbeat_interval: float = 10.0,
        connection_timeout: float = 10.0,
        buffer_size: int = 2048,
        auto_reconnect: bool = True
    ):
        self.host = host
        self.port = port
        self.reconnect_delay = reconnect_delay
        self.max_reconnect_delay = max_reconnect_delay
        self.heartbeat_interval = heartbeat_interval
        self.connection_timeout = connection_timeout
        self.buffer_size = buffer_size
        self.auto_reconnect = auto_reconnect

        self._socket: Optional[socket.socket] = None
        self._state = ConnectionState.DISCONNECTED
        self._state_lock = threading.Lock()

        self._running = False
        self._receive_thread: Optional[threading.Thread] = None
        self._heartbeat_thread: Optional[threading.Thread] = None
        self._reconnect_thread: Optional[threading.Thread] = None

        self._send_queue: Queue = Queue()
        self._send_thread: Optional[threading.Thread] = None

        self._current_reconnect_delay = reconnect_delay
        self._reconnect_attempts = 0

        self.on_message: Optional[Callable[[bytes], None]] = None
        self.on_connection_change: Optional[Callable[[ConnectionState], None]] = None
        self.on_error: Optional[Callable[[Exception], None]] = None

    @property
    def state(self) -> ConnectionState:
        with self._state_lock:
            return self._state

    @state.setter
    def state(self, new_state: ConnectionState):
        with self._state_lock:
            if self._state != new_state:
                self._state = new_state
                logger.info(f"Stan połączenia: {new_state.value}")
                if self.on_connection_change:
                    try:
                        self.on_connection_change(new_state)
                    except Exception as e:
                        logger.error(f"Błąd w callbacku on_connection_change: {e}")

    @property
    def is_connected(self) -> bool:
        return self.state == ConnectionState.CONNECTED

    def connect(self) -> bool:
        if self.is_connected:
            logger.warning("Już połączono")
            return True

        self._running = True
        self.state = ConnectionState.CONNECTING

        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.settimeout(self.connection_timeout)
            self._socket.connect((self.host, self.port))
            self._socket.settimeout(None)

            self.state = ConnectionState.CONNECTED
            self._current_reconnect_delay = self.reconnect_delay
            self._reconnect_attempts = 0

            self._start_threads()

            logger.info(f"Połączono z {self.host}:{self.port}")
            return True

        except socket.error as e:
            logger.error(f"Błąd połączenia: {e}")
            self._handle_connection_error(e)
            return False

    def _start_threads(self):
        self._receive_thread = threading.Thread(target=self._receive_loop, daemon=True)
        self._receive_thread.start()

        self._send_thread = threading.Thread(target=self._send_loop, daemon=True)
        self._send_thread.start()

        if self.heartbeat_interval > 0:
            self._heartbeat_thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
            self._heartbeat_thread.start()

    def _receive_loop(self):
        while self._running and self.is_connected:
            try:
                if self._socket is None:
                    break

                data = self._socket.recv(self.buffer_size)

                if not data:
                    logger.info("Serwer zamknął połączenie")
                    self._handle_disconnect()
                    break

                if self.on_message:
                    try:
                        self.on_message(data)
                    except Exception as e:
                        logger.error(f"Błąd w callbacku on_message: {e}")

            except socket.timeout:
                continue
            except socket.error as e:
                if self._running:
                    logger.error(f"Błąd odbioru: {e}")
                    self._handle_disconnect()
                break

    def _send_loop(self):
        while self._running:
            try:
                data = self._send_queue.get(timeout=1.0)
                if data is None:
                    break

                if self.is_connected and self._socket:
                    try:
                        self._socket.sendall(data)
                    except socket.error as e:
                        logger.error(f"Błąd wysyłania: {e}")
                        self._handle_disconnect()
                else:
                    self._send_queue.put(data)
                    time.sleep(0.5)

            except Exception:
                continue

    def _heartbeat_loop(self):
        while self._running and self.is_connected:
            time.sleep(self.heartbeat_interval)

            if not self._running or not self.is_connected:
                break

            try:
                if self._socket:
                    self._socket.send(b'')
            except socket.error as e:
                logger.warning(f"Heartbeat failed: {e}")
                self._handle_disconnect()
                break

    def _handle_disconnect(self):
        was_connected = self.is_connected
        self._close_socket()

        if was_connected and self.auto_reconnect and self._running:
            self.state = ConnectionState.RECONNECTING
            self._start_reconnect()
        else:
            self.state = ConnectionState.DISCONNECTED

    def _handle_connection_error(self, error: Exception):
        self._close_socket()

        if self.on_error:
            try:
                self.on_error(error)
            except Exception as e:
                logger.error(f"Błąd w callbacku on_error: {e}")

        if self.auto_reconnect and self._running:
            self.state = ConnectionState.RECONNECTING
            self._start_reconnect()
        else:
            self.state = ConnectionState.DISCONNECTED

    def _start_reconnect(self):
        if self._reconnect_thread and self._reconnect_thread.is_alive():
            return

        self._reconnect_thread = threading.Thread(target=self._reconnect_loop, daemon=True)
        self._reconnect_thread.start()

    def _reconnect_loop(self):
        while self._running and self.state == ConnectionState.RECONNECTING:
            self._reconnect_attempts += 1
            logger.info(f"Próba ponownego połączenia #{self._reconnect_attempts} za {self._current_reconnect_delay:.1f}s...")

            time.sleep(self._current_reconnect_delay)

            if not self._running:
                break

            try:
                self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self._socket.settimeout(self.connection_timeout)
                self._socket.connect((self.host, self.port))
                self._socket.settimeout(None)

                self.state = ConnectionState.CONNECTED
                self._current_reconnect_delay = self.reconnect_delay
                self._reconnect_attempts = 0

                self._start_threads()

                logger.info(f"Ponownie połączono z {self.host}:{self.port}")
                return

            except socket.error as e:
                logger.warning(f"Próba połączenia nieudana: {e}")
                self._close_socket()

                self._current_reconnect_delay = min(
                    self._current_reconnect_delay * 1.5,
                    self.max_reconnect_delay
                )

        if not self._running:
            self.state = ConnectionState.DISCONNECTED

    def _close_socket(self):
        if self._socket:
            try:
                self._socket.shutdown(socket.SHUT_RDWR)
            except Exception:
                pass
            try:
                self._socket.close()
            except Exception:
                pass
            self._socket = None

    def send(self, data: bytes | str) -> bool:
        if isinstance(data, str):
            data = data.encode('utf-8')

        if not self._running:
            logger.warning("Klient nie jest uruchomiony")
            return False

        self._send_queue.put(data)
        return True

    def send_now(self, data: bytes | str) -> bool:
        if isinstance(data, str):
            data = data.encode('utf-8')

        if not self.is_connected or not self._socket:
            logger.warning("Nie połączono - nie można wysłać")
            return False

        try:
            self._socket.sendall(data)
            return True
        except socket.error as e:
            logger.error(f"Błąd wysyłania: {e}")
            self._handle_disconnect()
            return False

    def disconnect(self):
        logger.info("Rozłączanie...")
        self._running = False
        self.auto_reconnect = False
        self._send_queue.put(None)

        self._close_socket()
        self.state = ConnectionState.DISCONNECTED

        for thread in [self._receive_thread, self._send_thread, self._heartbeat_thread, self._reconnect_thread]:
            if thread and thread.is_alive():
                thread.join(timeout=2.0)

        logger.info("Rozłączono")

    def reconnect(self):
        logger.info("Wymuszam ponowne połączenie...")
        self._close_socket()
        self._current_reconnect_delay = self.reconnect_delay
        self._reconnect_attempts = 0
        self.state = ConnectionState.RECONNECTING
        self._running = True
        self.auto_reconnect = True
        self._start_reconnect()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
        return False

if __name__ == "__main__":
    def on_message(data: bytes):
        print(f"📩 Otrzymano: {data.decode('utf-8', errors='replace')}")

    def on_state_change(state: ConnectionState):
        print(f"🔌 Stan połączenia: {state.value}")

    def on_error(error: Exception):
        print(f"❌ Błąd: {error}")

    client = TCPClient(
        host="localhost",
        port=8080,
        reconnect_delay=2.0,
        heartbeat_interval=10.0,
        auto_reconnect=True
    )

    client.on_message = on_message
    client.on_connection_change = on_state_change
    client.on_error = on_error

    print("Łączenie z serwerem...")
    client.connect()

    try:
        while True:
            msg = input("Wpisz wiadomość (lub 'quit' aby wyjść): ")
            if msg.lower() == 'quit':
                break
            if msg.lower() == 'reconnect':
                client.reconnect()
            elif msg:
                client.send(msg)
    except KeyboardInterrupt:
        print("\nPrzerwano")
    finally:
        client.disconnect()
