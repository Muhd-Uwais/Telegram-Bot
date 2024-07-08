# import requests
#
#
# class EspCommands:
#     TCP_IP = "192.168.1.75"
#
#     def __init__(self):
#         pass
#
#     def send_command(self, command):
#
#         comm = "/"
#         url = f"http://{self.TCP_IP}{comm}"  # Build complete URL
#         try:
#             reply = requests.post(url, data={"command": command})
#             reply.raise_for_status()  # Raise exception for non-200 status codes
#             return reply.text
#         except requests.exceptions.RequestException as e:
#             print(f"Error sending command: {e}")
#             return None
#
#
# if __name__ == "__main__":
#     # Example usage
#     communicator = EspCommands()  # Replace with actual IP
#     response = communicator.send_command("off")
#
#     if response:
#         print(response)
#         print("Command sent successfully!")
#     else:
#         print("An error occurred while sending the command.")


import socket


class EspCommands:
    TCP_IP = "192.168.1.72"
    TCP_PORT = 80

    # def __init__(self):
    #    self.data = None
    #    self.sock = None

    def send_command(self, command):
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.TCP_IP, self.TCP_PORT))
            sock.sendall(command.encode())
        except ConnectionError:
            data = "ConnectionError: Unable to connect to ESP32"
        except TimeoutError:
            data = "TimeoutError: Connection to ESP32 timed out"
        except OSError as e:
            data = f"OSError: {e}"
        finally:
            if sock is not None:
                sock.close()


if __name__ == "__main__":
    esp = EspCommands()
    esp.send_command(command="on")
