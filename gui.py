import os
import sys
import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk
from tkinter.messagebox import showinfo

from device_detector import DeviceDetector
from PIL import Image, ImageTk
from tkintertable import TableCanvas, TableModel

from color_swatch import color_swatch
from device_clustering import DeviceClustering

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

dir_path = os.path.dirname(os.path.realpath(__file__))

class Ui_IoTShield:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Cyber IoT Shield")
        self.loading_popup = None
        timeout_value = 2  # You can set this value according to your needs
        self.device_detector = DeviceDetector(num_threads=timeout_value)

        self.root.title("AI IoT Shield")
        self.root.geometry("840x780")

        self.root.config(bg="purple")
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        # self.create_buttons()  # Remove this line
        self.create_listbox()
        self.create_labels()
        self.create_entry_fields()
        self.create_widgets()

        self.frame_1 = tk.Frame(self.root, bg="white")
        self.frame_1.pack(side="left", fill="both",
                          expand=True, padx=10, pady=10)
        self.frame_2 = tk.Frame(self.root, bg="white")
        self.frame_2.pack(side="left", fill="both",
                          expand=True, padx=10, pady=10)

        self.frame_3 = tk.Frame(self.root, bg="white")
        self.frame_3.pack(side="bottom", fill="both",
                          expand=True, padx=10, pady=10)

    # Remove the entire create_buttons method

    def create_listbox(self):
        self.device_listbox = tk.Listbox(self.main_frame)
        self.device_listbox.grid(row=1, column=0, padx=10, pady=10)

    def create_labels(self):
        self.device_label = tk.Label(self.main_frame, text="Devices")
        self.device_label.grid(row=2, column=0, padx=10, pady=10)

    def create_entry_fields(self):
        self.device_entry = tk.Entry(self.main_frame)
        self.device_entry.grid(row=3, column=0, padx=10, pady=10)

    def create_widgets(self):
        self.show_devices_button = ttk.Button(
            self.main_frame, text="Show Devices", command=self.show_devices)
        self.show_devices_button.grid(row=4, column=0, padx=10, pady=10)

    def show_devices(self):
        devices = self.device_detector.some_other_method_name()  # Update this line with the correct method name
        self.device_detector.update_devices_table(devices)
        for device in devices:
            self.device_listbox.insert(tk.END, device)

if __name__ == "__main__":
    root = tk.Tk()
    app = Ui_IoTShield(root)
    root.mainloop()
