import tkinter as tk
from tkinter import messagebox
import logging
from getmac import get_mac_address
import tkinter.ttk as ttk
from device import IoTDevice
from device_detection import DeviceDetector
from gui import Ui_IoTShield
from iot_network import IoTNetwork
from pdf_report import generate_pdf
from report_issue import report_issue
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

class MainWindow:
    _last_child_ids = None
    
    def __init__(self):
        self.tk = tk.Tk()
        self.tk.title("IoT Shield")
        self.ui = Ui_IoTShield(self)  # pass self as an argument
        self.ui.setup_ui()
        self.detector = DeviceDetector()
        self.loading_popup = None
        # Set the close button event
        self.tk.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.ui.hide_loading_popup()
        self.destroy()

if __name__ == "__main__":
    main_window = MainWindow()
    main_window.mainloop()
