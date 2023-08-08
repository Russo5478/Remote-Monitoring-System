from tkinter import Tk
from variables import ethernet_ip
from functions import window_geometry, center_window, create_button, create_button_image, create_label, create_frame, \
    w_f, h_f
from Devices.DevMain import view_computers


class AdminPanel:
    def __init__(self, admin_window):
        self.adapter = ethernet_ip

        self.ap_init = admin_window
        self.screen_width = 1000
        self.screen_height = 700
        window_geometry(self.ap_init, 1000, 700)
        self.ap_init.title("REMOTE ADMIN - ADMIN PANEL")
        self.ap_init.resizable(0, 0)
        self.ap_init.configure(background="#c4c4c4")

        self.current_frame = "dashboard"
        self.alert_count = 0
        self.add_comp_window = None
        self.first_check = None
        self.first_connection_process = None
        self.first_check_info = None

        center_window(self.ap_init)
        self.load_main_widgets()

    def load_main_widgets(self):
        top_bar_background = "#111111"
        top_bar = create_frame(self.ap_init, 0, 0, self.screen_width, 50)
        top_bar.configure(background=top_bar_background)

        logo_frame = create_frame(self.ap_init, 0, 0, 60, 50)
        logo_frame.configure(background="#f59a27")

        create_button_image('assets/bell.png', top_bar, self.screen_width - w_f(70), h_f(8), (32, 30),
                            top_bar_background)

        alert_count = create_label(top_bar, self.screen_width - w_f(40), h_f(10), (str(self.alert_count) + "+"), 9)
        alert_count.configure(background=top_bar_background, fg="white")
        alert_count.config(font=('yu gothic ui', 9, "bold"))

        title_label = create_label(top_bar, 80, 3, "ipMonitor", 18)
        title_label.configure(background=top_bar_background, fg="white")
        title_label.config(font=('yu gothic ui', 18, "bold"))

        dashboard_button = create_button(top_bar, 220, 5, "Dashboard")
        dashboard_button.configure(font=("yu gothic ui", w_f(12), "bold"), background=top_bar_background, fg="white",
                                   relief="flat")
        
        def comps_func():
            view_computers(self.ap_init, self.screen_width, self.screen_height)

        machines_button = create_button(top_bar, 330, 5, "Devices")
        machines_button.configure(font=("yu gothic ui", w_f(12), "bold"), background=top_bar_background, fg="white",
                                  relief="flat", command=comps_func)

        reports_button = create_button(top_bar, 415, 5, "Reports")
        reports_button.configure(font=("yu gothic ui", w_f(12), "bold"), background=top_bar_background, fg="white",
                                 relief="flat")

        configuration_button = create_button(top_bar, 500, 5, "Configuration")
        configuration_button.configure(font=("yu gothic ui", w_f(12), "bold"), background=top_bar_background, fg="white"
                                       , relief="flat")
        

def admin_win():
    admin_initializer = Tk()
    admin_initializer.iconbitmap("assets/net.ico")
    AdminPanel(admin_initializer)
    admin_initializer.mainloop()


admin_win()
