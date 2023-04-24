import tkinter as tk
from tkinter import messagebox

from getmac import get_mac_address

from device import IoTDevice
from device_detection import DeviceDetector
from gui import Ui_IoTShield
from iot_network import IoTNetwork
from pdf_report import generate_pdf
from report_issue import report_issue

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Cyber IoT Shield")
        self.geometry("1024x800")
        self.resizable(False, False)
        
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.ui = Ui_IoTShield(self)  # Pass the reference to the MainWindow instance
        self.ui.setup_ui()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def scan_devices(self):
        detector = DeviceDetector()
        devices = detector.scan_devices()
        self.ui.update_device_table(devices)

    def on_close(self):
        # Handle any cleanup tasks here
        print("Closing the application...")
        self.destroy()

if __name__ == "__main__":
    main_window = MainWindow()
    main_window.mainloop()