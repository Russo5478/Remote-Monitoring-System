from socket import socket, AF_INET, SOCK_STREAM
from hashlib import md5
from pickle import dumps


def start_server(ip_address: str, port: int, number: int):
    connection = socket(AF_INET, SOCK_STREAM)
    communication_address = (ip_address, port)
    connection.bind(communication_address)

    print("Attempting to start server!")
    connection.listen(number)

    while True:
        try:
            print(f"Listening for new connections on {ip_address}:{port}")
            client_socket, client_address = connection.accept()
            print(f"Connection accepted from: {client_address[0]}:{client_address[1]}")

            return client_socket, client_address

        except OSError as e:
            if e.errno == 10048:
                print("encounter stubborn error!")
                continue


def client_connect(ip_address: str, port: int):
    connection = socket(AF_INET, SOCK_STREAM)

    try:
        communication_address = (ip_address, port)
        connection.settimeout(3)
        connection.connect(communication_address)
        print(f"Successfully connected to {ip_address}:{port}")

        return connection

    except ConnectionRefusedError:
        return False

    except TimeoutError:
        return False

    except OSError as e:
        if e.errno == 10065:
            return False

    except SystemExit:
        print("exit")
        return False


def authentication(connection, pass_key: str, identity):
    pre_handshake = str(md5(pass_key.encode()).hexdigest())
    auth_payload = dumps([pre_handshake, identity])

    try:
        connection.send(auth_payload)
        authentication_response = str(connection.recv(1024).decode())

        return True if authentication_response == "success" else False

    except KeyboardInterrupt:
        pass
