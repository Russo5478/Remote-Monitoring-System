from time import strftime
from sqlite3 import connect
from PIL import Image, ImageTk
from screeninfo import get_monitors
from tkinter.ttk import Label as Tl
from ctypes import windll as window_dpi
from tkinter import Label, Frame, PhotoImage, Button, Toplevel, Entry
from variables import default_font, default_database, original_height_factor, original_width_factor

window_dpi.shcore.SetProcessDpiAwareness(1)


db = default_database


def w_f(d):
    width_factor = get_monitors()[0].width / get_monitors()[0].width_mm
    return int((d * width_factor) / original_width_factor)


def h_f(d):
    height_factor = get_monitors()[0].height / get_monitors()[0].height_mm
    return int((d * height_factor) / original_height_factor)


def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2) - 30

    window.geometry(f"{width}x{height}+{x}+{y}")


def create_image(image_path, parent, pos_x, pos_y, wxh, back):
    image_file = Image.open(image_path).resize(wxh)
    image_name = ImageTk.PhotoImage(image_file)
    image_label = Label(parent, image=image_name, bg=back)
    image_label.image = image_name
    image_label.place(x=w_f(pos_x), y=h_f(pos_y))


def create_button_image(image_path, parent, pos_x, pos_y, wxh, back):
    image_file = Image.open(image_path).resize(wxh)
    image_name = ImageTk.PhotoImage(image_file)
    image_button = Button(parent, image=image_name, bg=back, relief="flat")
    image_button.image = image_name
    image_button.place(x=w_f(pos_x), y=h_f(pos_y))

    return image_button


def create_gif(gif_path, parent, pos_x, pos_y, width, height, speed):
    open_gif = Image.open(gif_path)
    frames = open_gif.n_frames

    gif_object = [PhotoImage(file=gif_path, format=f"gif -index {i}") for i in range(frames)]

    def animation(count):
        new_image = gif_object[count]

        gif_label.configure(image=new_image)
        count += 1
        if count == frames:
            count = 0

        parent.after(speed, lambda: animation(count))

    gif_label = Label(parent)
    gif_label.place(x=w_f(pos_x), y=h_f(pos_y), width=w_f(width), height=h_f(height))

    animation(5)


def create_label(parent, pox_x: int, pos_y: int, text: str, font_size: int):
    label = Label(parent, text=text)
    label.configure(font=(default_font, w_f(font_size)))
    label.place(x=w_f(pox_x), y=h_f(pos_y))

    return label

def window_geometry(tk_class, width: int, height: int):
    tk_class.geometry(f"{w_f(width)}x{h_f(height)}")


def create_frame(parent, pox_x: int, pos_y: int, width: int, height: int):
    frame = Frame(parent)
    frame.place(x=w_f(pox_x), y=h_f(pos_y), width=w_f(width), height=h_f(height))

    return frame


def create_button(parent, pox_x: int, pos_y: int, text: str):
    button = Button(parent, text=text)
    button.place(x=w_f(pox_x), y=h_f(pos_y))

    return button


def create_entry(parent, pox_x, pos_y, font: tuple):
    entry = Entry(parent)
    entry.configure(font=font)
    entry.place(x=w_f(pox_x), y=h_f(pos_y))

    return entry


def get_current_time():
    current_time = strftime('%d/%B/%Y %H:%M')

    return str(current_time)


def database_all_lookup(db_path: str, what_selection: str, from_selection: str):
    db_connection = connect(db_path)
    writer = db_connection.cursor()
    lookup_command = "SELECT {} FROM {}".format(what_selection, from_selection)
    writer.execute(lookup_command)
    result = writer.fetchall()
    db_connection.close()

    return result


def database_specified_lookup(db_path: str, what_selection: str, from_selection: str, where_selection: str,
                              value_select):
    db_connection = connect(db_path)
    writer = db_connection.cursor()
    lookup_command = "SELECT {} FROM {} WHERE {} ='{}'".format(what_selection, from_selection, where_selection,
                                                               value_select)
    writer.execute(lookup_command)
    result = writer.fetchall()
    db_connection.close()

    return result


def database_like_lookup(db_path: str, what_selection: str, from_selection: str, where_selection: str, value_select):
    db_connection = connect(db_path)
    writer = db_connection.cursor()
    lookup_command = "SELECT {} FROM {} WHERE {} LIKE '{}'".format(what_selection, from_selection, where_selection,
                                                                   value_select)
    writer.execute(lookup_command)
    result = writer.fetchall()
    db_connection.close()

    return result


def database_update(db_path: str, what_selection: str, set_selection: str, new_value, where_selection: str,
                    value_select):
    db_connection = connect(db_path)
    writer = db_connection.cursor()
    lookup_command = "UPDATE {} SET {}='{}' WHERE {}='{}'".format(what_selection, set_selection, new_value,
                                                                  where_selection, value_select)
    writer.execute(lookup_command)
    db_connection.close()


def database_delete(db_path: str, from_selection: str, where_selection: str, value_select):
    db_connection = connect(db_path)
    writer = db_connection.cursor()
    lookup_command = "DELETE FROM {} WHERE {}='{}'".format(from_selection, where_selection, value_select)
    writer.execute(lookup_command)
    db_connection.close()


def database_insert(db_path: str, into_selection: str, new_values: tuple):
    values_length = len(new_values)
    number_of_commas = '?' * values_length
    comma_parameters = ','.join(number_of_commas[i:i + 1] for i in range(0, len(number_of_commas), 1))
    parameters = '(' + comma_parameters + ')'

    db_connection = connect(db_path)
    writer = db_connection.cursor()

    lookup_command = "INSERT INTO {} VALUES {}".format(into_selection, parameters)
    writer.execute(lookup_command, new_values)

    db_connection.commit()
    db_connection.close()


class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.tooltip_text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        x = self.widget.winfo_rootx() + self.widget.winfo_width() + 2
        y = self.widget.winfo_rooty()
        self.tooltip = Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = Tl(self.tooltip, text=self.tooltip_text, background="#ffffe0", relief="solid")
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip is not None:
            self.tooltip.destroy()
            self.tooltip = None