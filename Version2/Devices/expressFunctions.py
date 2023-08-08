from re import match
from tkinter import TclError, Label, messagebox
from tkinter.ttk import Combobox, Treeview
from PIL import Image, ImageTk
from functions import w_f, h_f, database_specified_lookup, create_label, create_frame, center_window, \
    database_all_lookup, window_geometry, create_button, database_insert
from variables import default_database, connect_key, ethernet_ip
from threading import Thread
from connections import authentication, client_connect
from pickle import loads


class ExpressFunctions:
    def __init__(self, main_parent, label_parent, ip_entry, ip_btn):
        self.express_init = main_parent
        self.entry_frame = label_parent
        self.ip_entry = ip_entry
        self.ip_btn = ip_btn

        self.connection_port = 63333
        self.first_connection_success = None
        self.full_information = None
        self.image_label = None

        self.widget_interaction()

    def widget_interaction(self):
        ip_address = self.ip_entry.get().strip()
        pattern = r'^(\d{1,3}\.){3}\d{1,3}$'

        if match(pattern, ip_address):
            print(f"Scanning for {ip_address}")
            image_file = Image.open("assets/loading.png").resize((25, 25))
            image_name = ImageTk.PhotoImage(image_file)
            image_label = Label(self.entry_frame, image=image_name, bg="#ededed")
            image_label.image = image_name
            image_label.place(x=w_f(475), y=h_f(50))
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

            self.ip_entry.configure(state='readonly')
            self.ip_btn.configure(state='disabled')

            ip_check = database_specified_lookup(default_database, "*", "computers", "ethernetIpv4", ip_address)
            client_connection = client_connect(ip_address, self.connection_port)

            if len(ip_check) == 0 and client_connection:
                success = authentication(client_connection, connect_key, ethernet_ip)

                if success:
                    first_connection_process = Thread(target=self.first_connection, args=(client_connection,))
                    first_connection_process.start()

                    def check_completion():
                        print("Checking")
                        if self.first_connection_success is False:
                            image_label.destroy()
                            self.express_init.update_idletasks()

                            self.ip_entry.configure(state="normal")
                            self.ip_entry.delete(0, "end")
                            self.ip_btn.configure(state="normal")
                            self.ip_entry.focus_set()

                        elif self.first_connection_success:
                            self.completion()

                        else:
                            self.express_init.after(1000, check_completion)

                    self.express_init.after(1000, check_completion)

                else:
                    messagebox.showerror(f"Error connecting to {ip_address}",
                                         "Check you are connected or the client software is running in target machine")
                    self.first_connection_success = False

            elif not client_connection:
                messagebox.showwarning("Error connecting", f"The IP Address {ip_address} cannot be located. " 
                                                           "If the target is offline perform a reconnect!")
                image_label.destroy()

                self.ip_entry.configure(state="normal")
                self.ip_btn.configure(state="normal")
                self.ip_entry.focus_set()
                self.express_init.update_idletasks()

            else:
                messagebox.showwarning("Duplicate", f"The IP Address {ip_address} has already been added. "
                                                    "If the target is offline perform a reconnect!")
                image_label.destroy()

                self.ip_entry.configure(state="normal")
                self.ip_btn.configure(state="normal")
                self.ip_entry.focus_set()
                self.express_init.update_idletasks()

        else:
            messagebox.showerror("Invalid IP", "Ensure that the address entered is a valid IPv4 address")
            self.ip_entry.focus_set()

    def first_connection(self, connection):
        print("Initiating first connection")
        connection.send(b'first_connection')
        first_information = loads(connection.recv(4092))
        print(first_information)

        if first_information:
            self.full_information = first_information
            self.first_connection_success = True

        else:
            print("Could not receive all info")
            connection.close()
            self.image_label.destroy()
            self.ip_entry.configure(state="normal")
            self.ip_entry.delete(0, "end")
            self.ip_btn.configure(state="normal")
            self.ip_entry.focus_set()
            self.express_init.update_idletasks()
            self.first_connection_success = False

        connection.close()

    def completion(self):
        self.first_connection_success = None

        self.image_label.destroy()
        self.express_init.update_idletasks()
        window_geometry(self.express_init, 560, 480)
        self.entry_frame.place(x=w_f(20), y=h_f(140), width=w_f(520), height=h_f(320))
        center_window(self.express_init)

        room_group_label = create_label(self.entry_frame, 20, 270, "Select Room/Group", 11)
        room_group_label.configure(background="#ededed")

        room_groups = database_all_lookup(default_database, "roomName", "rooms")

        rooms_combo = Combobox(self.entry_frame)
        rooms_combo['values'] = room_groups
        rooms_combo.configure(font=('yu gothic ui', w_f(11)), state='readonly', justify='center')
        rooms_combo.place(x=w_f(180), y=h_f(270), width=w_f(150))

        specs_frame = create_frame(self.entry_frame, 20, 100, 455, 150)
        specs_frame.configure(background="green")

        specs_cols = ("Specs", "Description")
        top_tree = Treeview(specs_frame, columns=specs_cols, show="headings", selectmode="none")
        top_tree.pack(side="left", fill="both", expand=1)

        top_tree.heading("#1", text="Specification", anchor="center")
        top_tree.heading("#2", text="Description", anchor="center")
        top_tree.column("#1", anchor="w")
        top_tree.column("#2", anchor="center")

        top_tree.tag_configure("odd", background="#eee")
        top_tree.tag_configure("even", background="#ddd")

        top_tree.insert('', 'end',
                        values=("Operating System", f"{self.full_information[0][0]} "
                                                    f"{self.full_information[0][3]}"),
                        tags=("odd", "row"))

        top_tree.insert('', 'end',
                        values=("Computer Name", f"{self.full_information[0][1]}"),
                        tags=("even", "row"))

        top_tree.insert('', 'end',
                        values=("Total RAM", f"{int(self.full_information[2][0] / 1000000000)} GB"),
                        tags=("odd", "row"))

        top_tree.insert('', 'end',
                        values=("Ethernet Mac", f"{self.full_information[8][0]}"),
                        tags=("even", "row"))

        top_tree.insert('', 'end',
                        values=("Screen Resolution", f"{self.full_information[4][0]}x"
                                                     f"{self.full_information[4][1]}"),
                        tags=("odd", "row"))

        top_tree.insert('', 'end',
                        values=("Running Processes", f"{self.full_information[3][-1]}"),
                        tags=("even", "row"))

        last_id = database_all_lookup(default_database, "ID", "computers")

        save_btn = create_button(self.entry_frame, 360, 265, "SAVE")
        save_btn.configure(background="green", fg="white", relief="solid",
                           font=('yu gothic ui', 12), width=w_f(10), command=self.save_computer)

        def save_shortcut(event):
            self.save_computer(last_id, rooms_combo)

        self.express_init.bind('<Return>', save_shortcut)

    def save_computer(self, last_id, rooms_combo):
        try:
            if rooms_combo.get().strip() != "":
                new_id = int(last_id[-1][0]) + 1
                new_comp_values = (
                    new_id, self.full_information[0][1], rooms_combo.get(),
                    self.full_information[0][0], self.full_information[0][3],
                    self.full_information[1][3], self.full_information[1][0],
                    self.full_information[1][2], self.full_information[1][1],
                    self.full_information[1][4], int(self.full_information[2][0] / 1000000000),
                    f"{self.full_information[4][0]}x{self.full_information[4][1]}",
                    f"{self.full_information[5][0]}x{self.full_information[5][1]}",
                    self.full_information[7][1], self.full_information[7][0],
                    self.full_information[8][1], self.full_information[8][0],
                    (self.full_information[9][1]) / 1000,
                    self.full_information[9][0] / 1000)

                comp_connection = (new_id, self.full_information[8][1], 1, 0)

                database_insert(default_database, "computers", new_comp_values)
                database_insert(default_database, "connections", comp_connection)
                messagebox.showinfo("Success", f"{self.full_information[0][1]} "
                                               f"was added successfully!")

                self.express_init.destroy()

            else:
                messagebox.showwarning("Group / Room Missing",
                                       "Please select a room or group to proceed")
                self.express_init.focus_set()

        except IndexError:
            new_id = 0
            if rooms_combo.get().strip() != "":
                new_comp_values = (
                    new_id, self.full_information[0][1], rooms_combo.get(),
                    self.full_information[0][0], self.full_information[0][3],
                    self.full_information[1][3], self.full_information[1][0],
                    self.full_information[1][2], self.full_information[1][1],
                    self.full_information[1][4], int(self.full_information[2][0] / 1000000000),
                    f"{self.full_information[4][0]}x{self.full_information[4][1]}",
                    f"{self.full_information[5][0]}x{self.full_information[5][1]}",
                    self.full_information[7][1], self.full_information[7][0],
                    self.full_information[8][1], self.full_information[8][0],
                    (self.full_information[9][1]) / 1000,
                    self.full_information[9][0] / 1000)

                comp_connection = (new_id, self.full_information[8][1], 1, 0)

                database_insert(default_database, "computers", new_comp_values)
                database_insert(default_database, "connections", comp_connection)
                messagebox.showinfo("Success", f"{self.full_information[0][1]} "
                                               f"was added successfully!")

                self.express_init.destroy()

            else:
                messagebox.showwarning("Group / Room Missing",
                                       "Please select a room or group to proceed")
                self.express_init.focus_set()




