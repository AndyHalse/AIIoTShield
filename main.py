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

if __name__ == '__main__':
    main_window = MainWindow()