import os
import socket

file_upload = "commands.txt"
file_new_name = "cm.txt"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("172.16.10.128", 63333))

file = open(file_upload, "rb")
file_size = os.path.getsize(file_upload)

client.send(file_new_name.encode())
client.send(str(file_size).encode())

print(client.recv(1024).decode())

data = file.read()
client.sendall(data)
client.send(b"<END>")

file.close()
client.close()
