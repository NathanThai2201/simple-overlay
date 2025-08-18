import tkinter as tk
from PIL import Image, ImageTk
from AppKit import NSApp, NSStatusWindowLevel
from pynput import keyboard
import threading

clickthrough_enabled = False
win = None

def set_clickthrough(state: bool):
    global win, clickthrough_enabled
    app = NSApp()
    windows = app.windows()
    if windows:
        win = windows[0]
        win.setLevel_(NSStatusWindowLevel)
        win.setIgnoresMouseEvents_(state)
        win.orderFront_(None)
        clickthrough_enabled = state
        print("Click-through:", "ON" if state else "OFF")

def toggle_clickthrough_mainthread():
    global clickthrough_enabled
    set_clickthrough(not clickthrough_enabled)

def hotkey_listener():
    def on_activate():
        root.after(0, toggle_clickthrough_mainthread)

        # Hotkey set is "T"
    with keyboard.GlobalHotKeys(
        {'T': on_activate}) as h:
        h.join()

def resize(event=None):
    """Resize background image to fit window"""
    global global_image
    img_width, img_height = base_image.size
    scale = min(root.winfo_width() / img_width,
                root.winfo_height() / img_height)

    new_width = int(img_width * scale)
    new_height = int(img_height * scale)

    resized = base_image.resize((new_width, new_height))
    global_image = ImageTk.PhotoImage(resized)
    background_label.config(image=global_image)






root = tk.Tk()
root.title("Screen Overlay")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}+0+0")
root.attributes('-alpha', 0.2)


base_image = Image.open("a.png")

global_image = ImageTk.PhotoImage(base_image)

background_label = tk.Label(root, image=global_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# text_label = tk.Label(root, text="Hello!!!",
#                       bg="#000000", fg="white")
# text_label.pack(pady=20, expand=True)

# bind resize event
root.bind("<Configure>", resize)

# start with click-through
root.after(300, lambda: set_clickthrough(True))

# hotkey listener thread
listener_thread = threading.Thread(target=hotkey_listener, daemon=True)
listener_thread.start()

root.mainloop()
