from socket import socket, AF_INET, SOCK_STREAM
from psutil import net_if_addrs, virtual_memory, process_iter, disk_partitions, disk_usage, net_io_counters
from hashlib import md5
from pickle import dumps, loads
from cpuinfo import get_cpu_info
from screeninfo import get_monitors
from platform import uname
from time import sleep
from threading import Thread


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


class MainClient:
    def __init__(self):
        network_adapters = net_if_addrs()
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.port1 = 63333
        self.adapter = network_adapters['Ethernet'][1].address if 'Ethernet' in network_adapters else '0.0.0.0'
        communication_address = (str(self.adapter), self.port1)
        self.socket.bind(communication_address)
        self.all_information = collect_information()

        self.net_pass = "*REMOTEADMIN#"
        self.listener()

    def listener(self):
        print("Starting listener")
        self.socket.listen(1)

        while True:
            try:
                print(f"Listening for new connections on {self.adapter}:{self.port1}")
                client_socket, client_address = self.socket.accept()
                print(f"Connection accepted from: {client_address[0]}:{client_address[1]}")

                self.initialization(client_socket)
                client_socket.close()
                print("Completed closing connection!")

            except SystemExit:
                self.socket.close()

            except OSError as e:
                if e.errno == 10048:
                    continue

    def initialization(self, client_connection):
        password_auth, main_server_ip = loads((client_connection.recv(1024)))

        if self.authenticator(password_auth):
            client_connection.send(b'success')
            print("Authentication Success!")
            command = client_connection.recv(1024).decode()

            if command == "first_connection":
                print("First connection--")
                # Remember to receive settings
                client_connection.send(dumps(self.all_information))
                client_connection.close()

            else:
                print("Unknown command")
                client_connection.close()

            client_connection.close()

        else:
            client_connection.send(b'Connection Rejected')
            client_connection.close()

    def authenticator(self, received_auth: str):
        pre_handshake = str(md5(self.net_pass.encode()).hexdigest())

        return True if pre_handshake == received_auth else False


if __name__ == '__main__':
    MainClient()
