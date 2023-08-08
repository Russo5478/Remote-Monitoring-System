from scapy.all import *
from scapy.layers.inet import TCP, IP


def packet_callback(packet):
    # Filter packets with TCP protocol
    if packet.haslayer(TCP):
        try:
            src_ip = packet[IP].src

            if str(src_ip) == '172.217.170.206':
                print("Abnnormal activity")

        except IndexError:
            sniff(prn=packet_callback, filter="tcp")


def start_packet_capture():
    # Start capturing packets and pass them to the packet_callback function
    sniff(prn=packet_callback, filter="tcp")


start_packet_capture()
