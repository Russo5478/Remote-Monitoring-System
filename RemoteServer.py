import tkinter
import keyboard


root = tkinter.Tk()
root.attributes('-fullscreen', True)


def block_keyboard():
    keyboard.block_key("Alt")
    keyboard.block_key("F4")
    keyboard.block_key("Ctrl")
    keyboard.block_key("Shift")
    keyboard.block_key("Escape")
    keyboard.block_key("D")
    keyboard.block_key("d")
    keyboard.block_key("Delete")
    keyboard.block_key("Win")


root.after(1000, block_keyboard)
root.mainloop()

# screenshot = ImageGrab.grab()
# screenshot.save("Image.png")
