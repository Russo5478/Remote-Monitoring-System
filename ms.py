from socket import socket, AF_INET, SOCK_STREAM
from psutil import net_if_addrs, virtual_memory, process_iter, disk_partitions, disk_usage, net_io_counters
from hashlib import md5
from pickle import dumps, loads
from cpuinfo import get_cpu_info
from screeninfo import get_monitors
from platform import uname
from time import sleep
from threading import Thread
from pickle import loads, dumps
from multiprocessing import Process

# =============================== Global variables =====================================
port1 = 63333
network_adapters = net_if_addrs()
adapter = network_adapters['Ethernet'][1].address if 'Ethernet' in network_adapters else '0.0.0.0'
net_pass = "*REMOTEADMIN#"

server_socket = socket(AF_INET, SOCK_STREAM)


# ======================================================================================
def collect_information():
    all_information = []
    system_info = uname()
    cpu_information = get_cpu_info()
    ram_information = virtual_memory()
    net_io = net_io_counters()

    system_name = system_info.system
    system_node = system_info.node
    system_release = system_info.release
    system_version = system_info.version

    all_system_info = [system_name, system_node, system_release, system_version]
    all_information.append(all_system_info)

    processor_brand = cpu_information['brand_raw']
    processor_bits = cpu_information['bits']
    processor_count = cpu_information['count']
    processor_vendor = cpu_information['vendor_id_raw']
    processor_speed = cpu_information['hz_advertised_friendly']

    all_cpu_info = [processor_brand, processor_bits, processor_count, processor_vendor, processor_speed]
    all_information.append(all_cpu_info)

    total_ram = ram_information.total
    available_ram = ram_information.available
    percent_used = 100 - ((int(available_ram) / int(total_ram)) * 100)

    all_ram_info = [total_ram, available_ram, percent_used]
    all_information.append(all_ram_info)

    processlist = []

    for processes in process_iter():
        processlist.append(processes.name())

    processlist.append(len(processlist))
    all_information.append(processlist)

    screen_resolution = [get_monitors()[0].width, get_monitors()[0].height]
    screen_size = [get_monitors()[0].width_mm, get_monitors()[0].height_mm]

    all_information.append(screen_resolution)
    all_information.append(screen_size)

    disks_information = []
    partitions = disk_partitions()
    for partition in partitions:
        try:
            partition_usage = disk_usage(partition.mountpoint)
            disks_information.append([partition.device, partition.mountpoint, partition.fstype,
                                      partition_usage.total, partition_usage.used, partition_usage.free,
                                      partition_usage.percent])

        except PermissionError:
            disks_information.append([partition.device, partition.mountpoint, partition.fstype,
                                      None, None, None, None])
            continue

    all_information.append(disks_information)

    wifi_mac = net_if_addrs()['Wi-Fi'][0].address if 'Wi-Fi' in net_if_addrs() else None
    wifi_ipv4 = net_if_addrs()['Wi-Fi'][1].address if 'Wi-Fi' in net_if_addrs() else None

    eth0_mac = net_if_addrs()['Ethernet'][0].address if 'Ethernet' in net_if_addrs() else None
    eth0_ipv4 = net_if_addrs()['Ethernet'][1].address if 'Ethernet' in net_if_addrs() else None

    wifi_addr = [wifi_mac, wifi_ipv4]
    ethernet_addr = [eth0_mac, eth0_ipv4]

    all_information.append(wifi_addr)
    all_information.append(ethernet_addr)

    network_usage = [net_io.bytes_sent, net_io.bytes_recv]
    all_information.append(network_usage)

    return all_information


def initialization(client_connection):
    password_auth, main_server_ip = loads((client_connection.recv(1024)))

    if authenticator(password_auth):
        client_connection.send(b'success')
        print("Authentication Success!")
        command = client_connection.recv(1024).decode()

        if command == "first_connection":
            print("First connection--")
            # Remember to receive settings
            all_information = collect_information()
            client_connection.send(dumps(all_information))

    else:
        client_connection.send(b'Connection Rejected')

    client_connection.close()


def authenticator(received_auth: str):
    pre_handshake = str(md5(net_pass.encode()).hexdigest())

    return True if pre_handshake == received_auth else False


def machine_control(sock):
    communication_address = (str(adapter), port1)
    sock.bind(communication_address)

    try:
        while True:
            sock.listen(1)

            # Accept a client connection
            client_socket, client_address = sock.accept()
            print(f"Connection accepted from: {client_address}")

            initialization(client_socket)

    except KeyboardInterrupt:
        # Close the server socket
        sock.close()


# def browser_monitor(sock):
#     # port = 64000
#     #
#     # # while True:
#     # #     try:
#     # #         sock = socket(AF_INET, SOCK_STREAM)
#     # #         communication_address = (str(eth0_ip), port)
#     # #         sock.connect(communication_address)
#     # #         break
#     # #
#     # #     except ConnectionRefusedError:
#     # #         print("Connection refused. Retrying in 10 seconds...")
#     # #         sleep(10)
#     # #         continue
#     #
#     # forbidden_addresses = ['172.217.170.206', '172.217.170.174']
#     # print("Connected")
#     #
#     # def forbidden_function():
#     #     mouse_listener = mouse.Listener(suppress=True)
#     #     keyboard_listener = keyboard.Listener(suppress=True)
#     #
#     #     root = Tk()
#     #     root.attributes('-fullscreen', True)
#     #
#     #     def block_input():
#     #         mouse_listener.start()
#     #         keyboard_listener.start()
#     #
#     #     def unblock_input():
#     #         mouse_listener.stop()
#     #         keyboard_listener.stop()
#     #         root.destroy()
#     #
#     #     block_input()
#     #
#     #     root.after(10000, unblock_input)
#     #     root.mainloop()
#     #
#     # def packet_callback(packet):
#     #     # Filter packets with TCP protocol
#     #     if packet.haslayer(TCP):
#     #         try:
#     #             src_ip = packet[IP].src
#     #
#     #             if str(src_ip) in forbidden_addresses:
#     #                 screenshot_path = grab_screenshot()
#     #                 forbidden_function()
#     #                 print("Abnormal activity")
#     #                 sleep(20)
#     #
#     #         except IndexError:
#     #             sniff(prn=packet_callback, filter="tcp")
#     #
#     # while True:
#     #     sniff(prn=packet_callback, filter="tcp")


if __name__ == "__main__":
    # Create a Process object for each task
    process1 = Process(target=machine_control, args=(server_socket,))

    # Start the processes
    process1.start()
