import socket
import time

from psutil import net_if_addrs
from pickle import dumps, loads
from tkinter import Tk, Button
from os import path
from pathlib import Path

# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

network_adapters = net_if_addrs()

if 'Ethernet' in network_adapters:
    self_ip = str(network_adapters['Ethernet'][1].address)

else:
    self_ip = '0.0.0.0'

port = 64000  # Port number to bind

# Bind the socket to the IP address and port
sock.bind(("172.16.10.129", port))
sock.listen(2)
print("Started connection! Listening")
client_socket, client_address = sock.accept()

raw_payload = ["93.184.216.34"]
bytes_py = dumps(raw_payload)

print('connected')

client_socket.send(bytes_py)
activity = client_socket.recv(1024)

if activity:
    filename = client_socket.recv(1024).decode('utf-8')
    file_size = client_socket.recv(1024).decode('utf-8')

    chunk = int(0.90 * float(file_size))

    documents_path = Path(path.expanduser("~/Documents"))
    storage_location = documents_path / "RMDownloads" / filename

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

    root = Tk()
    screen_width = root.winfo_screenwidth() // 2
    screen_height = root.winfo_screenheight() // 2

    window_width = 300
    window_height = 200

    window_x_placement = int(screen_width - (window_width / 2))
    window_y_placement = int(screen_height - (window_height / 2))

    root.geometry("{}x{}+{}+{}".format(window_width, window_height, window_x_placement, window_y_placement))
    root.wm_attributes('-topmost', 1)
    root.resizable(False, False)
    root.title("Abnormal activity detected!")

    def unblock():
        root.destroy()
        client_socket.send(dumps("Unblock"))

    close_button = Button(root, text="Unblock Interface", relief="solid", command=unblock)
    close_button.place(x=100, y=50)

    root.mainloop()

client_socket.close()
