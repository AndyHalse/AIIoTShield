import logging
import threading
import time
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
        self.main_frame = ttk.Frame(self, padding=(5, 5, 5, 5))
        self.main_frame.pack(fill="both", expand=True)

        self.ui = Ui_IoTShield(self.main_frame)  # Pass self.main_frame as argument
        self.ui.create_ui()
        self.ui.create_buttons()

        self.ui.setupUi(self)
        self.device_table = DeviceTable(self.ui.tableWidget)
        self.detector = NetworkDetector()

        self.ui.scan_button.config(command=self.start_scan)
        self.ui.save_to_pdf_button.config(command=self.on_save_to_pdf_button_clicked)
        self.ui.logs_button.config(command=self.on_logs_button_clicked)
        self.ui.help_button.config(command=self.on_help_button_clicked)

    def start_vulnerability_check_thread(self):
        vulnerability_check_thread = threading.Thread(target=run_vulnerability_check, daemon=True)
        vulnerability_check_thread.start()

    def start_scan(self):
        self.ui.message_label.config(text="Scanning...")
        self.ui._button.config(state=tk.DISABLED)
        self.detector.start_scan(self.update_device_table, self.scan_complete)

    def update_device_table(self, devices):
        self.ui.message_label.config(text=f"Detected {len(devices)} devices")
        self.device_table.update_table(devices)

    def scan_complete(self):
        self.ui._button.config(state=tk.NORMAL)

    def on_save_to_pdf_button_clicked(self):
        pass

    def on_logs_button_clicked(self):
        pass

    # Add this method to handle the closing event
    def on_close(self):
        # Perform any necessary cleanup before closing the application
        self.destroy()

if __name__ == "__main__":
    main_window = MainWindow()
    main_window.title("AI Cyber IoT Shield")
    main_window.iconbitmap("assets/logo.ico")
    main_window.resizable(False, False)
    main_window.protocol("WM_DELETE_WINDOW", main_window.on_close)

    main_window.frame = tk.Frame(main_window)
    main_window.frame.pack(side="top", fill="both", expand=True)

    main_window.detector = DeviceDetector(timeout=1)

    main_window.ui = Ui_IoTShield(
        main_window=main_window, reload_data_func=main_window.reload_data)

    main_window.ui.pack(side="top", fill="both", expand=True)

    print("Scanning for devices...")
    main_window.update_device_table(main_window.detector.scan_devices())

    main_window.mainloop()
