import logging
import tkinter as tk
from device_detection import DeviceDetector
from gui import Ui_IoTShield
from tkinter import Tk

# set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.ui = Ui_IoTShield(self.root, self)
        self.devices = []

    def scan_devices(self):
        # Add code to scan for devices here
        self.devices = ["Device 1", "Device 2", "Device 3"]
        self.ui.update_device_list(self.devices)

if __name__ == '__main__':
    main_window = MainWindow()