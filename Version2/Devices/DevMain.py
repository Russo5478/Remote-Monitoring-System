from ttkthemes import ThemedStyle
from tkinter import Frame, Menu, StringVar
from functions import w_f, h_f, create_label, create_entry, create_button_image, Tooltip, database_all_lookup, \
    create_frame
from tkinter.ttk import Treeview, Scrollbar
from variables import default_database
from Devices.expressWidgets import ExpressWidgets
from Devices.autoscanWidgets import ScanWidgets


def view_computers(main_parent, screen_width, screen_height):
    search_words = StringVar()
    devices_frame = create_frame(main_parent, 5, 50, screen_width - w_f(20), screen_height - h_f(60))
    devices_frame.configure(background="#c4c4c4")

    title_text = create_label(devices_frame, 10, 5, "Devices", 15)
    title_text.configure(fg="#000", background="#c4c4c4")
    title_text.config(font=("yu gothic ui", 15, "bold"))

    table_control = create_frame(devices_frame, 20, 51, screen_width - w_f(47), screen_height - h_f(660))
    table_control.configure(background="#fbfbfb")

    search_label = create_label(table_control, 20, 7, "Search", 12)
    search_label.configure(font=('yu gothic ui', w_f(12)), background="#fbfbfb")
    search_label.config(font=("yu gothic ui", 12, "bold"))

    search_entry = create_entry(table_control, 80, 8, ("yu gothic ui", w_f(12)))
    search_entry.configure(justify='center', relief='solid', width=w_f(40), textvariable=search_words)

    def add_comp():
        ExpressWidgets(main_parent)

    def auto_scan():
        ScanWidgets(main_parent)

    add_computer = create_button_image('assets/computer.png', table_control, 800, 5, (26, 25), "#fbfbfb")
    add_group = create_button_image('assets/add-group.png', table_control, 850, 5, (24, 22), "#fbfbfb")
    auto_search = create_button_image('assets/detect.png', table_control, 900, 5, (25, 23), "#fbfbfb")
    add_computer.configure(command=add_comp)
    auto_search.configure(command=auto_scan)

    Tooltip(add_computer, "Add Computer")
    Tooltip(add_group, "Add Room/Group")
    Tooltip(auto_search, "Auto Detect")

    vc_area = Frame(devices_frame)
    vc_area.configure(background="blue")
    vc_area.place(x=w_f(19), y=h_f(91), width=screen_width - w_f(45), height=screen_height - h_f(320))

    interface_style = ThemedStyle(vc_area)
    interface_style.theme_use("clearlooks")
    interface_style.configure("Treeview", font=("Verdana", 10), foreground="#2b2b2b", cellpadding=w_f(10))
    interface_style.configure("Treeview.Heading", font=("Verdana", 10, "bold"), foreground="#444",
                              background="silver")
    interface_style.map("Treeview", background=[('selected', 'lightblue')], foreground=[('selected', 'orange')])

    top_scrollbar = Scrollbar(vc_area, orient="vertical")
    top_scrollbar.pack(side="right", fill="y")

    bot_scrollbar = Scrollbar(vc_area, orient="horizontal")
    bot_scrollbar.pack(side="bottom", fill="x")

    top_columns = ("Machine Name", "IP Address", "MAC Address", "Room", "Connection")
    top_tree = Treeview(vc_area, columns=top_columns, show="headings", selectmode="browse")
    top_tree.pack(side="left", fill="both", expand=1)

    top_tree.heading("#1", text="Computer Name", anchor="center")
    top_tree.heading("#2", text="IP Address", anchor="center")
    top_tree.heading("#3", text="MAC Address", anchor="center")
    top_tree.heading("#4", text="Room/Building", anchor="center")
    top_tree.heading("#5", text="Connection", anchor="center")

    top_tree.column("#1", anchor="center", width=w_f(150))
    top_tree.column("#2", anchor="center")
    top_tree.column("#3", anchor="center")
    top_tree.column("#4", anchor="center")
    top_tree.column("#5", anchor="center", width=w_f(100))

    top_tree.tag_configure("odd", background="#eee")
    top_tree.tag_configure("even", background="#ddd")
    top_tree.configure(yscrollcommand=top_scrollbar.set)
    top_scrollbar.configure(command=top_tree.yview)

    top_tree.configure(xscrollcommand=bot_scrollbar.set)
    bot_scrollbar.configure(command=top_tree.xview)

    def popup(event):
        top_tree.focus_set()
        row_id = top_tree.identify_row(event.y)
        top_tree.selection_set(row_id)
        row_values = top_tree.item(row_id)['values']
        print(row_values)

        pop_menu = Menu(top_tree, tearoff=0, font=("Verdana", 9))
        pop_menu.add_command(label="Transfer", accelerator="Ctrl+E")
        pop_menu.add_command(label="Reconnect")
        pop_menu.add_command(label="Delete")
        pop_menu.add_separator()
        pop_menu.add_command(label="Set timer")
        pop_menu.add_command(label="Screenshot")
        pop_menu.add_command(label="Send File")
        pop_menu.add_command(label="Terminal")
        pop_menu.add_command(label="Message")
        pop_menu.add_command(label="Video Playback")
        pop_menu.add_separator()
        pop_menu.add_command(label="Unblock")
        pop_menu.add_command(label="Lock")
        pop_menu.add_command(label="Shutdown")
        pop_menu.post(event.x_root, event.y_root)

    top_tree.tag_bind("row", "<Button-3>", lambda event: popup(event))

    machines = database_all_lookup(default_database, "*", "computers")
    connection = database_all_lookup(default_database, "*", "connections")

    for i in range(0, len(machines)):
        if i % 2 == 0:
            for z in range(0, len(connection)):
                if connection[z][1] == machines[i][-4] and connection[z][2] == 1:
                    top_tree.insert('', 'end',
                                    values=(machines[i][1], machines[i][-4], machines[i][-3], machines[i][2],
                                            "online"), tags=("even", "row"))

                elif connection[z][1] == machines[i][-4] and connection[z][2] == 0:
                    top_tree.insert('', 'end',
                                    values=(machines[i][1], machines[i][-4], machines[i][-3], machines[i][2],
                                            "offline"), tags=("even", "row"))

        else:
            for z in range(0, len(connection)):
                if connection[z][1] == machines[i][-4] and connection[z][2] == 1:
                    top_tree.insert('', 'end',
                                    values=(machines[i][1], machines[i][-4], machines[i][-3], machines[i][2],
                                            "online"), tags=("odd", "row"))

                elif connection[z][1] == machines[i][-4] and connection[z][2] == 0:
                    top_tree.insert('', 'end',
                                    values=(machines[i][1], machines[i][-4], machines[i][-3], machines[i][2],
                                            "offline"), tags=("odd", "row"))

    def ip_filter(*args):
        items_on_treeview = top_tree.get_children()
        search = search_entry.get().lower()

        for item in items_on_treeview:
            values = top_tree.item(item)['values']
            for value in values:
                if search in str(value).lower():
                    search_var = values
                    top_tree.delete(item)
                    top_tree.insert("", 0, values=search_var)
                    break  # Exit the loop after finding a match in any value

    def filtered_popup(event):
        item = top_tree.identify_row(event.y)
        top_tree.selection_set(item)
        row_values = top_tree.item(item)['values']
        print(row_values)

        pop_menu = Menu(top_tree, tearoff=0, font=("Verdana", 9))
        pop_menu.add_command(label="Transfer", accelerator="Ctrl+E")
        pop_menu.add_command(label="Reconnect")
        pop_menu.add_command(label="Delete")
        pop_menu.add_separator()
        pop_menu.add_command(label="Set timer")
        pop_menu.add_command(label="Screenshot")
        pop_menu.add_command(label="Send File")
        pop_menu.add_command(label="Terminal")
        pop_menu.add_command(label="Message")
        pop_menu.add_command(label="Video Playback")
        pop_menu.add_separator()
        pop_menu.add_command(label="Unblock")
        pop_menu.add_command(label="Lock")
        pop_menu.add_command(label="Shutdown")
        pop_menu.post(event.x_root, event.y_root)

    top_tree.bind("<Button-3>", filtered_popup, add="+")

    search_words.trace('w', ip_filter)

    bottom_title = create_label(devices_frame, 25, 475, "System Specifications", 12)
    bottom_title.configure(font=("yu gothic ui", 12, "bold"), bg='#c4c4c4')

    bottom_frame = create_frame(devices_frame, 20, 505, screen_width - w_f(45), screen_height - h_f(570))
    bottom_frame.configure(background="#fbfbfb")

    comp_ip = create_label(bottom_frame, w_f(10), h_f(5), "IP Address:", 12)
    comp_ip.configure(font=('yu gothic ui', w_f(12), "bold"), bg='#fbfbfb')
    comp_ip_value = create_label(bottom_frame, w_f(100), h_f(6), "192.154.100.200", 11)
    comp_ip_value.configure(font=('yu gothic ui', w_f(11), "bold"), bg='#fbfbfb', fg='green')

    comp_ram = create_label(bottom_frame, w_f(10), h_f(33), "RAM:", 12)
    comp_ram.configure(font=('yu gothic ui', w_f(12), "bold"), bg='#fbfbfb')
    comp_ram_value = create_label(bottom_frame, w_f(100), h_f(34), "Total: 8.00GB Available: 3.00", 11)
    comp_ram_value.configure(font=('yu gothic ui', w_f(11), "bold"), bg='#fbfbfb', fg='green')

    comp_hdd = create_label(bottom_frame, w_f(10), h_f(62), "Hard Disk:", 12)
    comp_hdd.configure(font=('yu gothic ui', w_f(12), "bold"), bg='#fbfbfb')
    comp_hdd_value = create_label(bottom_frame, w_f(100), h_f(63), "Total: 500GB Available: 250GB", 11)
    comp_hdd_value.configure(font=('yu gothic ui', w_f(11), "bold"), bg='#fbfbfb', fg='green')

    comp_cpu = create_label(bottom_frame, w_f(10), h_f(90), "CPU:", 12)
    comp_cpu.configure(font=('yu gothic ui', w_f(12), "bold"), bg='#fbfbfb')
    comp_cpu_value = create_label(bottom_frame, w_f(100), h_f(91), "Intel Core i5-8350U @ 1.90GHz", 11)
    comp_cpu_value.configure(font=('yu gothic ui', w_f(11), "bold"), bg='#fbfbfb', fg='green')