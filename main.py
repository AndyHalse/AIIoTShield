import tkinter as tk

from device_detector import DeviceDetector

from device_clustering import DeviceClustering
from gui import Ui_IoTShield

class AIIoTShield(tk.Toplevel):
    def __init__(self, main_window):
        tk.Toplevel.__init__(self, main_window)

        self.device_detector = DeviceDetector()
        # Set up the UI
        self.ui = Ui_IoTShield(self)
        self.ui.setupUi()

        # Connect signals and slots
        self.ui.reload_data_button.clicked.connect(self.scan_devices)
        self.update_device_list([])

    def scan_devices(self):
        """

        """
        devices = self.device_detector.scan_devices()
        device_clustering = DeviceClustering(devices)
        clustered_devices = device_clustering.cluster_devices()

        self.update_device_list(clustered_devices)

    def update_device_list(self, devices):
        # Update the device list UI
        pass

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI Cyber IoT Shield")

        self.root.mainloop()

if __name__ == "__main__":
    MainWindow()
