from psutil import net_if_addrs

default_font = "yu gothic ui"
default_database = "assets/master.db"
ethernet_ip = net_if_addrs()['Ethernet'][0].address if 'Ethernet' in net_if_addrs() else '0.0.0.0'
original_width_factor = 1600 / 309
original_height_factor = 900 / 174
connect_key = "*REMOTEADMIN#"