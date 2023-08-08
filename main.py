import time
from psutil import net_if_addrs
from flask import Flask, render_template, request, jsonify
import webbrowser
import sqlite3
from CommandCenter import individual_server_coms
from os import remove
from os.path import getsize
from socket import socket, AF_INET, SOCK_STREAM
from hashlib import md5
from base64 import b64encode
from multiprocessing import Process
import os
from pathlib import Path


app = Flask(__name__)

network_adapters = net_if_addrs()

if 'Ethernet' in network_adapters:
    eth0_ip = str(network_adapters['Ethernet'][1].address)

else:
    eth0_ip = '0.0.0.0'


def browser():
    sock = socket(AF_INET, SOCK_STREAM)
    port = 64000

    sock.bind((eth0_ip, port))
    sock.listen(10)

    while True:
        client_socket, client_address = sock.accept()
        print(f"Connection accepted from: {client_address}")


def send_files(ip, f_location, f_name):
    port = 63333
    sock = socket(AF_INET, SOCK_STREAM)
    command = "send"
    handshake = md5(str(ip).encode()).hexdigest()
    new_command = str(handshake) + "+" + command

    try:
        # Connect to the remote computer
        sock.connect((ip, port))

        # Send the command
        sock.send(new_command.encode())

        file = open(str(f_location), "rb")
        file_size = (getsize(str(f_location)))

        sock.send(b64encode(f_name.encode('utf-8')))
        time.sleep(1)
        sock.send(b64encode(str(file_size).encode('utf-8')))

        data = file.read()
        sock.sendall(data)
        sock.send(b"<END>")

        file.close()
        sock.close()

    except ConnectionRefusedError:
        print(f"Could not connect to {ip}:{port}")

    finally:
        # Close the socket
        sock.close()


@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/labs.html')
def labs():
    # Connect to the SQLite database
    conn = sqlite3.connect('master.db')
    cursor = conn.cursor()

    # Execute a query to retrieve data
    cursor.execute('SELECT * FROM Comp_labs')

    # Fetch all rows from the result set
    rows = cursor.fetchall()

    # Close the database connection
    cursor.close()
    conn.close()

    # Pass the data to the template and render it
    return render_template('labs.html', data=rows)


@app.route('/traffic.html')
def traffic():
    # Pass the data to the template and render it
    return render_template('traffic.html')


@app.route('/comps')
def retrieve_data():
    name = request.args.get('name')

    # Connect to the SQLite database
    conn = sqlite3.connect('master.db')
    cursor = conn.cursor()

    # Execute a query to retrieve data based on the name
    cursor.execute('SELECT compLab, ipAddress, motherboardNumber FROM Computers WHERE compLab = ?', (name,))
    rows = cursor.fetchall()

    # Close the database connection
    cursor.close()
    conn.close()

    # Convert the retrieved data into a list of dictionaries
    data = [{'column1': row[0], 'column2': row[1], 'column3': row[2]} for row in rows]

    # Return the data as a JSON response
    return jsonify(data)


@app.route('/shutdown', methods=['POST'])
def individual_shutdown():
    data = request.get_json()
    ip_address = data.get('ip')
    individual_server_coms(str(ip_address), "shutdown /s /f /t 0")

    # Return a response if needed
    return {'message': 'Shutdown command received'}


@app.route('/lock', methods=['POST'])
def individual_lock():
    data = request.get_json()
    ip_address = data.get('ip')
    individual_server_coms(str(ip_address), "rundll32.exe user32.dll,LockWorkStation")

    # Return a response if needed
    return {'message': 'Lock command received'}


@app.route('/gather_info', methods=['POST'])
def gather_info():
    data = request.get_json()
    ip_address = data.get('ip')
    individual_server_coms(str(ip_address), "info")

    # Return a response if needed
    return {'message': 'Info command received'}


@app.route('/process-file', methods=['POST'])
def process_file():
    file = request.files['file']
    ip_address = request.form['ipAddress']

    documents_path = Path(os.path.expanduser("~/Documents"))
    local_storage_location = documents_path / "RM" / file.filename
    file.save(local_storage_location)
    print(f"File saved at: {local_storage_location}")
    file.close()

    send_files(ip_address, local_storage_location, file.filename)
    remove(local_storage_location)

    # Return a response if needed
    return 'File processed successfully'


def open_browser():
    url = "http://127.0.0.1:5000"
    webbrowser.open(url)


if __name__ == '__main__':
    browser_control = Process(target=browser)
    browser_control.start()

    open_browser()
    app.run(debug=True)
