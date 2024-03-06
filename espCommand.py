import socket
import time

class EspCommands:
    TCP_IP = "192.168.1.72"
    TCP_PORT = 80

    def __init__(self):
        self.data = None
        self.sock = None

    def send_command(self, command):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.TCP_IP, self.TCP_PORT))
            self.sock.sendall(command.encode())
        except ConnectionError:
            self.data = "ConnectionError: Unable to connect to ESP32"
        except TimeoutError:
            self.data = "TimeoutError: Connection to ESP32 timed out"
        except OSError as e:
            self.data = f"OSError: {e}"
        finally:
            if self.sock is not None:
                self.sock.close()
