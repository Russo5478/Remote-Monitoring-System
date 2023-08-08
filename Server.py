import socket
import hashlib


class Server:
    def __init__(self):
        self.ipv4 = '172.16.10.99'
        self.port = 63333

    def command_sender(self, command):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Connect to the remote computer
            sock.connect((self.ipv4, self.port))

            # Send the command
            sock.sendall(command.encode())

            # Receive the response
            response = sock.recv(131072).decode()
            print(f"Response from {self.ipv4}: {response}")

        except ConnectionRefusedError:
            print(f"Could not connect to {self.ipv4}:{self.port}")


if __name__ == '__main__':
    Server()

