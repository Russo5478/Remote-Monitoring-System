import socket
import tqdm

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("172.16.10.128", 63333))
server.listen()

client, addr = server.accept()

file_name = client.recv(1024).decode()
print(file_name)
file_size = client.recv(1024).decode()
print(file_size)

client.send("Received".encode())

chunk = int(0.90 * float(file_size))

file = open(file_name, "wb")
file_bytes = b""

done = False
progress = tqdm.tqdm(unit="B", unit_scale=True, unit_divisor=1000, total=int(file_size))

while not done:
    data = client.recv(chunk)
    if file_bytes[-5:] == b"<END>":
        done = True
        file_bytes = file_bytes[:-5]

    else:
        file_bytes += data

    progress.update(chunk)

file.write(file_bytes)
client.close()
server.close()
