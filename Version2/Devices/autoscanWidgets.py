from tkinter import Toplevel, Text
from tkinter.ttk import Combobox
from functions import window_geometry, center_window, create_label, create_entry, create_image, create_frame, w_f, \
    create_button, h_f
from Devices.autoscanFunctions import AutoFunctions


class ScanWidgets:
    def __init__(self, parent_window):
        self.parent_window = parent_window
        self.scan_window = None
        self.scan_type = True

        self.express_widgets()

    def express_widgets(self):
        self.scan_window = Toplevel(self.parent_window)
        window_geometry(self.scan_window, 680, 270)
        self.scan_window.title("Scan IP Addresses")
        self.scan_window.configure(background="#fbfbfb")
        self.scan_window.resizable(False, False)
        self.scan_window.iconbitmap("assets/net.ico")

        center_window(self.scan_window)

        top_title = create_label(self.scan_window, 10, 5, "Auto Scan", 16)
        top_title.configure(font=("yu gothic ui", 16, "bold"), bg="#fbfbfb")

        create_image('assets/network.png', self.scan_window, 20, 55, (60, 60), "#fbfbfb")

        tip_text1 = "Alternate between IP Address Range and IP Address Lists. Note that scan times"
        tip_text2 = "will take longer for a larger network range or list. For a list range scan,"
        tip_text3 = "type the IPv4 addresses separated by a comma e.g. {192.1.1.1, 192.2.2.2}"

        tip1 = create_label(self.scan_window, 90, 55, tip_text1, 11)
        tip1.configure(bg="#fbfbfb")

        tip2 = create_label(self.scan_window, 90, 75, tip_text2, 11)
        tip2.configure(bg="#fbfbfb")

        tip3 = create_label(self.scan_window, 90, 95, tip_text3, 11)
        tip3.configure(bg="#fbfbfb")

        entry_frame = create_frame(self.scan_window, 20, 140, 640, 110)
        entry_frame.configure(background="#ededed", highlightthickness=2, highlightcolor="#c4c4c4")

        ip_entry_label = create_label(entry_frame, 10, 15, "IP Range:", 12)
        ip_entry_label.configure(bg="#ededed")

        ip_entry = create_entry(entry_frame, 95, 15, ('yu gothic ui', 14))
        ip_entry.configure(width=w_f(15), justify='center', relief='solid', background='#cccccc')
        ip_entry.focus_set()

        to_entry_label = create_label(entry_frame, 265, 15, "to", 12)
        to_entry_label.configure(bg="#ededed")

        to_entry = create_entry(entry_frame, 305, 15, ('yu gothic ui', 14))
        to_entry.configure(width=w_f(15), justify='center', relief='solid', background='#cccccc')

        choices_list = ["IP Range", "IP List"]
        choices_combo = Combobox(entry_frame)
        choices_combo['values'] = choices_list
        choices_combo.configure(font=('yu gothic ui', w_f(11)), state='readonly', justify='center')
        choices_combo.place(x=w_f(490), y=h_f(15), width=w_f(130))
        choices_combo.set(choices_list[0])

        list_entry = Text(entry_frame)
        list_entry.configure(relief='solid')
        list_entry.place(x=w_f(95), y=h_f(15), width=w_f(370), height=h_f(75))

        def get_computer():
            AutoFunctions(self.scan_window, entry_frame, ip_entry, to_entry, ip_btn, list_entry, self.scan_type)

        ip_btn = create_button(entry_frame, 490, 50, "Start Scan")
        ip_btn.configure(fg="#000", background="#5bfc63", font=("yu gothic ui", 11, "bold"), relief="solid",
                         width=w_f(10), command=get_computer)

        def add_shortcut(event):
            get_computer()

        self.scan_window.bind("<Return>", add_shortcut)

        def ip_range_widgets():
            self.scan_type = True
            list_entry.place(x=5000, y=5000)
            ip_entry_label.configure(text="IP Range")

        def ip_list_widgets():
            self.scan_type = False
            list_entry.place(x=w_f(95), y=h_f(15), width=w_f(370), height=h_f(75))
            ip_entry_label.configure(text="IP List")

        ip_range_widgets()

        def on_combobox_selected(event):
            if choices_combo.get() == choices_list[0]:
                ip_range_widgets()

            elif choices_combo.get() == choices_list[1]:
                ip_list_widgets()

        choices_combo.bind("<<ComboboxSelected>>", on_combobox_selected)
