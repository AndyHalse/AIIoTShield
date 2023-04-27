import tkinter as tk
from tkinter import ttk
from device_detection import DeviceDetector

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Device Detector")
        timeout_value = 10  # You should define this variable with a valid value
        num_threads = 10  # You can set this value according to your needs

if __name__ == "__main__":
    app = App()
    app.mainloop()
