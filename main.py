import threading
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

from getmac import get_mac_address

from device import IoTDevice
from device_detection import DeviceDetector
from gui import Ui_IoTShield
from iot_network import IoTNetwork
from report_issue import report_issue
from settings import APP_NAME, APP_VERSION, MQTT_BROKER
from vulnerability_detection import detect_vulnerability, run_vulnerability_check

print(f"{APP_NAME} v{APP_VERSION} is connecting to MQTT broker at {MQTT_BROKER}")

iot_network = IoTNetwork()

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Cyber IoT Shield")
        self.geometry("800x600")
        self.resizable(False, False)
        self.start_vulnerability_check_thread()

        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.ui = Ui_IoTShield(self, self.main_frame)

        self.ui.create_ui()
        self.ui.create_buttons()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def start_vulnerability_check_thread(self):
        vulnerability_check_thread = threading.Thread(target=run_vulnerability_check, daemon=True)
        vulnerability_check_thread.start()

    def on_close(self):
        # Handle any cleanup tasks here
        print("Closing the application...")
        self.destroy()

if __name__ == "__main__":
    main_window = MainWindow()
    main_window.mainloop()
