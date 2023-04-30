import tkinter as tk
from tkinter import messagebox
from gui import CustomDeviceDetectorUI

if __name__ == "__main__":
    root = tk.Tk()
    root.title("IoTShield")
    root.geometry("800x600")

    # Handle closing the window
    def handle_close():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", handle_close)

    # Create the GUI
    app = CustomDeviceDetectorUI(root)

    # Run the GUI
    app.mainloop()
