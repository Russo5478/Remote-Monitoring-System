from tkinter import Toplevel
from functions import window_geometry, center_window, create_label, create_entry, create_image, create_frame, w_f, \
    create_button
from Devices.expressFunctions import ExpressFunctions


class ExpressWidgets:
    def __init__(self, parent_window):
        self.parent_window = parent_window
        self.add_comp_window = None

        self.express_widgets()

    def express_widgets(self):
        self.add_comp_window = Toplevel(self.parent_window)
        window_geometry(self.add_comp_window, 560, 280)
        self.add_comp_window.title("Add Computer")
        self.add_comp_window.configure(background="#fbfbfb")
        self.add_comp_window.resizable(False, False)
        self.add_comp_window.iconbitmap("assets/net.ico")

        center_window(self.add_comp_window)

        top_title = create_label(self.add_comp_window, 10, 5, "Express Discovery", 16)
        top_title.configure(font=("yu gothic ui", 16, "bold"), bg="#fbfbfb")

        create_image('assets/light-bulb.png', self.add_comp_window, 20, 55, (60, 60), "#fbfbfb")

        tip_text1 = "Providing an accurate IPv4 Address can help speed up the discovery"
        tip_text2 = "process, discover more devices using the auto detect function"
        tip_text3 = "and locate more machines to monitor"

        tip1 = create_label(self.add_comp_window, 90, 55, tip_text1, 11)
        tip1.configure(bg="#fbfbfb")

        tip2 = create_label(self.add_comp_window, 90, 75, tip_text2, 11)
        tip2.configure(bg="#fbfbfb")

        tip3 = create_label(self.add_comp_window, 90, 95, tip_text3, 11)
        tip3.configure(bg="#fbfbfb")

        entry_frame = create_frame(self.add_comp_window, 20, 140, 520, 120)
        entry_frame.configure(background="#ededed", highlightthickness=2, highlightcolor="#c4c4c4")

        ip_entry_label = create_label(entry_frame, 20, 10, "Enter IP Address (Version 4):", 13)
        ip_entry_label.configure(bg="#ededed")

        ip_entry = create_entry(entry_frame, 23, 50, ('yu gothic ui', 14))
        ip_entry.configure(width=w_f(30), justify='center', relief='solid', background='#cccccc')
        ip_entry.focus_set()

        def get_computer():
            ExpressFunctions(self.add_comp_window, entry_frame, ip_entry, ip_btn)

        ip_btn = create_button(entry_frame, 345, 47, "Add Computer")
        ip_btn.configure(fg="#000", background="#5bfc63", font=("yu gothic ui", 11, "bold"), relief="solid",
                         width=w_f(13), command=get_computer)

        def add_shortcut(event):
            get_computer()

        self.add_comp_window.bind("<Return>", add_shortcut)
