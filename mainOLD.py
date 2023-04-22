import logging
import os
import socket
import tkinter as tk
import sys
from data_processing import DataProcessing
from device_detection import DeviceDetector
from gui import Ui_IoTShield

logging.basicConfig(filename='logs/iotshield.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

def on_log_button_clicked():
    log_file_path = "./logs/iotshield.log"
    os.system(f"open -a 'TextEdit' '{log_file_path}'")

def on_exit_button_clicked():
    sys.exit()

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Cyber IoT Shield")
        self.geometry("800x600")

        # Add a frame to the main window
        self.frame = tk.Frame(self)
        self.frame.pack(side="top", fill="both", expand=True)

        # Create an instance of DeviceDetector and Ui_IoTShield
        self.detector = DeviceDetector(
            DataProcessing().get_local_network_prefixes(socket.gethostbyname(socket.gethostname())), timeout=1)
        self.ui = Ui_IoTShield(main_window=self.frame, reload_data_func=self.reload_data)
        self.ui.pack(side="top", fill="both", expand=True)
        devices = self.detector.scan_devices()
        self.update_table(devices)
        self.ui.reload_data_button.config(command=self.reload_data)

    def on_plot_button_clicked(self):

        # Implement this method to plot the data
        pass

    def reload_data(self):

        try:
            self.ui.progressBar["value"] = 0
            self.ui.destroy()
            self.ui = Ui_IoTShield(main_window=self, reload_data_func=self.reload_data)
            ip_address = socket.gethostbyname(socket.gethostname())
            self.detector = DeviceDetector(
                DataProcessing().get_local_network_prefixes(socket.gethostbyname(socket.gethostname())), timeout=1)

            devices = self.detector.scan_devices()
            self.update_table(devices)
            self.ui.header_label.config(text="Data reloaded")
            logging.info("Data reloaded successfully")
            self.ui.reload_data_button.config(command=self.reload_data)
        except Exception as e:
            self.ui.header_label.config(text="Failed to reload data")
            logging.error(f"Failed to reload data: {str(e)}")

    def update_table(self, devices):

        self.ui.tableWidget.delete(*self.ui.tableWidget.get_children())
        for device in devices:
            icon = DataProcessing.get_device_icon(device["device_type"])
            self.ui.tableWidget.insert("", "end", values=(
            device["ip"], device["mac"], device["hostname"], device["device_type"], device["last_seen"], icon))

if __name__ == "__main__":
    app = tk.Tk()
    ui = MainWindow()
    app.mainloop()