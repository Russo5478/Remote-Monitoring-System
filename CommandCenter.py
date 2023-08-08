from socket import socket, AF_INET, SOCK_STREAM
from hashlib import md5


def command_center(command, ip):
    port = 63333
    sock = socket(AF_INET, SOCK_STREAM)

    try:
        # Connect to the remote computer
        sock.connect((ip, port))

        # Send the command
        sock.sendall(command.encode())

        # Receive the response
        response = sock.recv(131072).decode()
        print(f"Response from {ip}: {response}")

    except ConnectionRefusedError:
        print(f"Could not connect to {ip}:{port}")

    finally:
        # Close the socket
        sock.close()


def individual_server_coms(ipv4, comm):
    try:
        handshake = md5(str(ipv4).encode()).hexdigest()
        new_command = str(handshake) + "+" + comm
        command_center(new_command, ipv4)

    except KeyboardInterrupt:
        exit()
