import tkinter as tk
from gui import Ui_IoTShield
from device_detector import DeviceDetector
from device_clustering import DeviceClustering

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI Cyber IoT Shield")
        self.network = DeviceDetector(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299')
        self.ui = Ui_IoTShield(self.root, self, self.network)

    def scan_devices(self):
        print("Scanning devices...")
        devices = self.network.scan_devices()
        device_clustering = DeviceClustering(devices)
        clusters = device_clustering.cluster_devices()

        # Update the device list in the GUI with the scanned devices.
        # You need to implement this function in the Ui_IoTShield class.
        self.ui.update_device_list(clusters)

    def on_close(self):
        print("Closing application...")
        self.root.destroy()

if __name__ == "__main__":
    main_window = MainWindow()
