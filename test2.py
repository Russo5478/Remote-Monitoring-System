import socket

def get_all_ip_addresses(domain):
    try:
        ip_addresses = []
        addr_info = socket.getaddrinfo(domain, None)
        for info in addr_info:
            ip_addresses.append(info[4][0])
        return ip_addresses
    except socket.gaierror:
        return None


# Example usage
domain_name = "youtube.com"
ip_addresses = get_all_ip_addresses(domain_name)

if ip_addresses:
    print(f"The IP addresses of {domain_name} are:")
    for ip_address in ip_addresses:
        print(ip_address)
else:
    print(f"Failed to resolve IP addresses for {domain_name}")
