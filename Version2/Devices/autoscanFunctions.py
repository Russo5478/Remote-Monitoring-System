from re import match, findall
from tkinter import TclError, Label, messagebox, END
from tkinter.ttk import Combobox, Treeview
from PIL import Image, ImageTk
from functions import w_f, h_f, database_specified_lookup, create_label, create_frame, center_window, \
    database_all_lookup, window_geometry, create_button, database_insert
from variables import default_database, connect_key, ethernet_ip
from threading import Thread
from connections import authentication, client_connect
from pickle import loads


def subnet_check(ip1, ip2):
    def get_subnet(ip):
        ip_octets = ip.split('.')
        return '.'.join(ip_octets[:3])

    ip1_octets = ip1.split('.')
    ip2_octets = ip2.split('.')

    if len(ip1_octets) != 4 or len(ip2_octets) != 4:
        raise ValueError("Invalid IPv4 address format")

    subnet1 = get_subnet(ip1)
    subnet2 = get_subnet(ip2)

    return subnet1 == subnet2


def ip_integrity(ip1, ip2):
    ip1_octets = ip1.split('.')
    ip2_octets = ip2.split('.')

    for a, b in zip(ip1_octets, ip2_octets):
        if int(a) < int(b) <= 254:
            return True
        elif int(a) > int(b):
            return False

    return False


def first_connection(connection):
    print("Initiating first connection")
    connection.send(b'first_connection')
    first_information = loads(connection.recv(4092))

    if first_information:
        return first_information

    else:
        return False


class AutoFunctions:
    def __init__(self, main_parent, label_parent, ip_entry, to_entry, ip_btn, list_entry, scan_type):
        self.express_init = main_parent
        self.entry_frame = label_parent
        self.ip_entry = ip_entry
        self.to_entry = to_entry
        self.ip_btn = ip_btn
        self.scan_type = scan_type
        self.list_entry = list_entry

        self.connection_port = 63333
        self.scan_completion = False
        self.first_connection_success = None
        self.full_information = None
        self.image_label = None
        self.top_tree = None
        self.save_btn = None
        self.scan_list = []

        self.online_list = []
        self.offline_list = []

        self.online_count = "0"
        self.offline_count = "0"
        self.all_machine_info = []

        self.widget_interaction()

    def widget_interaction(self):
        if self.scan_type:
            start_point = self.ip_entry.get().strip()
            end_point = self.to_entry.get().strip()
            pattern = r'^(\d{1,3}\.){3}\d{1,3}$'

            if match(pattern, start_point) and match(pattern, end_point) and subnet_check(start_point, end_point) \
                    and ip_integrity(start_point, end_point):
                print(f"Scanning for {start_point} to {end_point}")
                image_file = Image.open("assets/loading.png").resize((25, 25))
                image_name = ImageTk.PhotoImage(image_file)
                image_label = Label(self.entry_frame, image=image_name, bg="#ededed")
                image_label.image = image_name
                image_label.place(x=w_f(595), y=h_f(53))
                self.image_label = image_label

                def rotate_image(angle):
                    try:
                        rotated_image = image_file.rotate(angle)
                        tk_image = ImageTk.PhotoImage(rotated_image)
                        image_label.configure(image=tk_image)
                        image_label.image = tk_image
                        angle += 10
                        if angle >= 360:
                            angle *= 0
                        self.express_init.after(20, rotate_image, angle)

                    except TclError:
                        pass

                rotate_image(0)

                self.ip_entry.configure(state='disabled')
                self.to_entry.configure(state='disabled')
                self.ip_btn.configure(state='disabled')

                ip1_octets = start_point.split('.')
                ip2_octets = end_point.split('.')
                count = 0

                while count < int(ip2_octets[3]) + 1:
                    if count == 0:
                        count = int(ip1_octets[3])

                    converted_ip = f"{ip1_octets[0]}.{ip1_octets[1]}.{ip1_octets[2]}.{str(count)}"
                    self.scan_list.append(converted_ip)
                    count += 1

                for ip_addresses in self.scan_list:
                    if database_specified_lookup(default_database, "*", "computers", "ethernetIpv4", ip_addresses):
                        self.scan_list.remove(ip_addresses)

                first_connection_process = Thread(target=self.list_scan)
                first_connection_process.start()

                def check_completion():
                    if self.scan_completion:
                        image_label.destroy()
                        self.express_init.update_idletasks()

                        completed_label = create_label(self.entry_frame, 95, 55, "Completed!", 12)
                        completed_label.configure(background="#ededed", foreground="green")
                        self.save_btn.configure(state="normal")

                    else:
                        self.express_init.after(1000, check_completion)

                self.express_init.after(1000, check_completion)

            else:
                messagebox.showerror("Invalid IP", "Ensure that the address entered is a valid IPv4 address\n"
                                                   "Ensure that the addresses are in the same subnet\n"
                                                   "Ensure that the address to is greater than start")
                self.ip_entry.focus_set()

        else:
            ip_lists = self.list_entry.get("1.0", END).strip()
            if ip_lists:
                ipv4_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'  # Regular expression pattern for IPv4 addresses

                # Find all occurrences of the IPv4 pattern in the content
                ipv4_addresses = findall(ipv4_pattern, ip_lists)
                print(ipv4_addresses)

            else:
                messagebox.showerror("Invalid Parameters", "No IPv4 Addresses were added!")
                self.list_entry.focus_set()

    def list_scan(self):
        if len(self.scan_list) > 0:
            window_geometry(self.express_init, 680, 510)
            center_window(self.express_init)
            self.entry_frame.place(height=h_f(350))

            specs_frame = create_frame(self.entry_frame, 95, 100, 455, 200)
            specs_frame.configure(background="green")

            specs_cols = ("IP Address", "Name", "RAM")
            self.top_tree = Treeview(specs_frame, columns=specs_cols, show="headings", selectmode="none")
            self.top_tree.pack(fill="both")

            self.top_tree.heading("#1", text="IPv4 Address", anchor="center")
            self.top_tree.heading("#2", text="Computer Name", anchor="center")
            self.top_tree.heading("#3", text="RAM", anchor="center")
            self.top_tree.column("#1", anchor="center", width=w_f(150))
            self.top_tree.column("#2", anchor="center")
            self.top_tree.column("#3", anchor="center", width=w_f(100))

            self.top_tree.tag_configure("odd", background="#eee")
            self.top_tree.tag_configure("even", background="#ddd")

            online_ip_label = create_label(self.entry_frame, 95, 305, "Online IP Addresses:", 11)
            online_ip_label.configure(bg="#ededed")

            online_ip_count = create_label(self.entry_frame, 240, 305, self.online_count, 11)
            online_ip_count.configure(bg="#ededed")

            offline_ip_label = create_label(self.entry_frame, 340, 305, "Offline IP Addresses:", 11)
            offline_ip_label.configure(bg="#ededed")

            offline_ip_count = create_label(self.entry_frame, 485, 305, self.offline_count, 11)
            offline_ip_count.configure(bg="#ededed")

            self.save_btn = create_button(self.entry_frame, 570, 305, "Save")
            self.save_btn.configure(fg="#000", background="#5bfc63", font=("yu gothic ui", 11, "bold"), relief="solid",
                                    command=self.compile_data, state="disabled")

            def save_shortcut(event):
                self.compile_data()

            self.express_init.bind("<Return>", save_shortcut)
            tag_count = 0

            for ip_address in self.scan_list:
                try:
                    client_connection = client_connect(ip_address, self.connection_port)

                    if client_connection:
                        authentication(client_connection, connect_key, ethernet_ip)
                        client_information = first_connection(client_connection)

                        if client_information:
                            client_connection.close()
                            self.online_list.append(ip_address)
                            self.online_count = str(len(self.online_list))
                            online_ip_count.configure(text=self.online_count)
                            self.all_machine_info.append(client_information)

                            if tag_count % 2 == 0:
                                self.top_tree.insert('', 'end', values=(client_information[8][1],
                                                                        client_information[0][1],
                                                                        client_information[2][0]), tags=('even', 'row'))

                            else:
                                self.top_tree.insert('', 'end', values=(client_information[8][1],
                                                                        client_information[0][1],
                                                                        client_information[2][0]), tags=('odd', 'row'))

                            tag_count += 1

                        else:
                            client_connection.close()
                            self.offline_list.append(ip_address)
                            self.offline_count = str(len(self.offline_list))
                            offline_ip_count.configure(text=self.offline_count)

                    else:
                        self.offline_list.append(ip_address)
                        self.offline_count = str(len(self.offline_list))
                        offline_ip_count.configure(text=self.offline_count)

                except RuntimeError:
                    exit()

                except TclError:
                    exit()

            self.scan_completion = True

        else:
            messagebox.showwarning("Invalid Parameters", "All IP Addresses are in database.\n"
                                                         "Run a reconnect scan.")

    def compile_data(self):
        last_id = database_all_lookup(default_database, "ID", "computers")
        
        if len(self.all_machine_info) > 0:
            for data in self.all_machine_info:
                try:
                    new_id = int(last_id[-1][0]) + 1
                    new_comp_values = (
                        new_id, data[0][1], "not assigned", data[0][0], data[0][3], data[1][3], data[1][0],
                        data[1][2], data[1][1], data[1][4], int(data[2][0] / 1000000000), f"{data[4][0]}x{data[4][1]}",
                        f"{data[5][0]}x{data[5][1]}", data[7][1], data[7][0], data[8][1], data[8][0],
                        (data[9][1]) / 1000, data[9][0] / 1000)

                    comp_connection = (new_id, data[8][1], 1, 0)

                    database_insert(default_database, "computers", new_comp_values)
                    database_insert(default_database, "connections", comp_connection)

                except IndexError:
                    new_id = 0
                    new_comp_values = (
                        new_id, data[0][1], "not assigned", data[0][0], data[0][3], data[1][3], data[1][0],
                        data[1][2], data[1][1], data[1][4], int(data[2][0] / 1000000000), f"{data[4][0]}x{data[4][1]}",
                        f"{data[5][0]}x{data[5][1]}", data[7][1], data[7][0], data[8][1], data[8][0],
                        (data[9][1]) / 1000, data[9][0] / 1000)

                    comp_connection = (new_id, data[8][1], 1, 0)

                    database_insert(default_database, "computers", new_comp_values)
                    database_insert(default_database, "connections", comp_connection)

            messagebox.showinfo("Success", f"{len(self.online_list)} IP Address(es) were saved successfully!")
            self.express_init.destroy()
                
        else:
            messagebox.showinfo("Empty Parameters", "No data will be saved!")
            self.express_init.destroy()
