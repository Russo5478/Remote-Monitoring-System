from flask import Flask, render_template, request
from configparser import ConfigParser, NoSectionError, NoOptionError
from os.path import exists
import webbrowser
import wmi
from psutil import net_if_addrs
from tkinter import messagebox, Tk, Button, Entry, Label

# ===============================================================
# Global Variables
product_code = None

app = Flask(__name__)


@app.route('/')
def home_page():
    return render_template('index.php')


@app.route('/submit', methods=['POST'])
def login_credentials():
    username = request.form.get('adminKey')
    password = request.form.get('password')

    print(username, password)
    return 'Form submitted successfully'


def open_browser():
    url = "http://127.0.0.1:5000"
    webbrowser.open(url)


def get_motherboard_serial_number():
    try:
        c = wmi.WMI()
        for board in c.Win32_BaseBoard():
            serial_number = board.SerialNumber
            if serial_number:
                return serial_number
        return None
    except wmi.x_wmi:
        return None


def get_mac_addresses():
    network_adapters = net_if_addrs()

    ethernet_macaddress = network_adapters['Ethernet'][0][1]
    wifi_macaddress = network_adapters['Wi-Fi'][0][1]

    return ethernet_macaddress, wifi_macaddress


def get_product_key():
    key_window = Tk()

    key_window.title("Product Key Information")
    key_window.geometry('400x200+400+200')
    key_window.resizable(False, False)

    product_code_label = Label(key_window)
    product_code_label.config(text='Product Code', font=('yu gothic ui', 13))
    product_code_label.place(x=30, y=20)

    product_code_entry = Entry(key_window)
    product_code_entry.config(relief='solid', justify='center', font=('yu gothic ui', 12))
    product_code_entry.place(x=155, y=22)

    def get_code():
        product_key = product_code_entry.get()
        print(product_key)
        key_window.destroy()

    submit_code = Button(key_window, command=get_code)
    submit_code.config(text='Submit', relief='solid', fg='white', bg='blue', font=('yu gothic ui', 11, 'bold'))
    submit_code.place(x=170, y=70)

    info_label = Label(key_window)
    info_label.configure(text='To get product key Please contact me @ \n'
                              'Tel: +254 790 559 143 \n'
                              'Gmail: mwangielvis49@gmail.com', fg='green')

    info_label.place(x=85, y=120)

    key_window.mainloop()


def config_file():
    config = ConfigParser()
    serial_number = get_motherboard_serial_number()
    eth0, wlan0 = get_mac_addresses()

    if not exists("config.ini"):
        # get_product_key()

        config.add_section('PC INFO')
        config.set('PC INFO', 'Motherboard', str(serial_number))
        config.set('PC INFO', 'Ethernet MAC', str(eth0))
        config.set('PC INFO', 'WiFi MAC', str(wlan0))

        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    else:
        try:
            config.read('config.ini')

            config_motherboard = config.get('PC INFO', 'Motherboard')
            config_eth0 = config.get('PC INFO', 'Ethernet MAC')
            config_wlan0 = config.get('PC INFO', 'WiFi MAC')

        except NoSectionError:
            get_product_key()

        except NoOptionError:
            get_product_key()

    config.read('config.ini')

    config_motherboard = config.get('PC INFO', 'Motherboard')
    config_eth0 = config.get('PC INFO', 'Ethernet MAC')
    config_wlan0 = config.get('PC INFO', 'WiFi MAC')

    if config_motherboard == serial_number or config_eth0 == eth0 or config_wlan0 == wlan0:
        print('good')

    else:
        messagebox.showerror('Failed Initialization', 'This product was copied from another PC \n Contact creator for '
                                                      'the software')


if __name__ == '__main__':
    # get_product_key()
    # # config_file()

    open_browser()
    app.run(debug=True)
