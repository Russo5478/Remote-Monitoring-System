import socket


def send_file(file_path, host, port):
    # Create a TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        sock.connect((host, port))

        # Open the file in binary mode
        with open(file_path, 'rb') as file:
            # Read and send the file in chunks
            while True:
                chunk = file.read(4096)  # Adjust the chunk size as per your requirements
                if not chunk:
                    break  # Reached the end of the file

                sock.sendall(chunk)

    except ConnectionRefusedError:
        print(f"Could not connect to {host}:{port}")

    finally:
        # Close the socket
        sock.close()


# Usage example
file_path = 'commands.txt'
host = '172.16.10.129'  # Replace with the server's IP address
port = 63333  # Replace with the server's port number

send_file(file_path, host, port)
