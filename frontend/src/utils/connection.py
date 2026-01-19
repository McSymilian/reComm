from logging import getLogger
import socket
logger = getLogger(__name__)


class Connection:

    def __init__(self, host: str = "192.168.100.44", port: int = 8080):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connect()
        logger.info(f"Connected to {self.host}:{self.port}")
    
    def __del__(self):
        self._disconnect()
 
    def _connect(self):
        self.socket.connect((self.host, self.port))

    def _disconnect(self):
        if self.socket:
            self.socket.close()
            self.socket = None

    def send(self, data: bytes):
        if not self.socket:
            raise ConnectionError("Not connected to server.")
        self.socket.sendall(data)

    def receive(self, buffer_size: int = 4096) -> bytes:
        if not self.socket:
            raise ConnectionError("Not connected to server.")
        return self.socket.recv(buffer_size)
    
    def close(self):
        self._disconnect()

if __name__ == "__main__":

    conn = Connection()
    conn.send(b"Hello, Server!")
    response = conn.receive()
    print(f"Received: {response.decode('utf-8')}")
    del conn