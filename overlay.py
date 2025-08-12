import tkinter as tk
from PIL import Image, ImageTk
from AppKit import NSApp, NSStatusWindowLevel

def raise_and_clickthrough():
    app = NSApp()
    windows = app.windows()
    if windows:
        win = windows[0]
        win.setLevel_(NSStatusWindowLevel)
        win.setIgnoresMouseEvents_(True)
        win.orderFront_(None)
        print("Window raised and click-through enabled.")
    else:
        print("No NSWindow found yet.")

root = tk.Tk()
root.title("Screen Overlay")
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
root.attributes('-alpha', 0.1)

image = Image.open("a.png")  
bg_image = ImageTk.PhotoImage(image)


background_label = tk.Label(root, image=bg_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)


# background color
text_label = tk.Label(root, bg="#000000", fg="black")
text_label.pack(pady=20, expand=True)

root.after(300, raise_and_clickthrough)

root.mainloop()
