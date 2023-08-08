from functions import center_window, create_image, create_gif, create_label, window_geometry
from ctypes import windll as window_dpi
from tkinter import Tk
# from RemoteWindow import admin_win

window_dpi.shcore.SetProcessDpiAwareness(1)


class SplashScreen:
    def __init__(self, splash_window):
        self.ss_init = splash_window
        self.splash_width = 500
        self.splash_height = 300

        window_geometry(self.ss_init, self.splash_width, self.splash_height)
        self.ss_init.title("REMOTE ADMIN")
        self.ss_init.resizable(0, 0)
        self.ss_init.overrideredirect(True)
        self.ss_init.wm_attributes('-topmost', 1)
        self.after_id = None

        center_window(self.ss_init)

        # ================================= SS Window Functions ========================================================
        self.load_main_widgets()

    def load_main_widgets(self):
        create_image("assets/Background.png", self.ss_init, 0, 0, (self.splash_width, self.splash_height), "blue")
        create_gif("assets/load.gif", self.ss_init, 200, 150, 100, 100, 30)

        loading_text_label = create_label(self.ss_init, 90, 100, "REMOTE ADMIN", 30)
        loading_text_label.configure(background="#1F41A9", fg="white")

        loading_texts_label = create_label(self.ss_init, 260, 278, ".........", 10)
        loading_texts_label.configure(background="#264ECA", fg="white")

        text_loaders = ["looking for database..........", "l", "g"]

        def change_text(index):
            loading_texts_label.configure(text=text_loaders[index])
            index = (index + 1) % len(text_loaders)

            if index != 0:
                self.after_id = loading_texts_label.after(1000, change_text, index)

            else:
                self.ss_init.after_cancel(self.after_id)
                self.ss_init.destroy()
                # admin_win()

        change_text(0)


def splash_screen():
    splash_initializer = Tk()
    SplashScreen(splash_initializer)
    splash_initializer.mainloop()

splash_screen()

