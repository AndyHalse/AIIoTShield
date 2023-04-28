import tkinter as tk
from tkinter import ttk

from device_detection import CustomDeviceDetector

class Ui_IoTShield(tk.Tk):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title("AI Cyber IoT Shield")
        self.geometry("1080x780")
        self.config(bg="purple")

        # Create the widgets for the UI
        self.create_widgets()

        # Create a frame for the main content
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill="both", expand=True)

        # Create the IP address entry widget and add it to the main frame using pack
        self.ip_entry = tk.Entry(self.main_frame)
        self.ip_entry.pack(side=tk.TOP, padx=10, pady=10)

        # Create a frame for the device detector
        self.device_detector_frame = tk.Frame(self.main_frame)
        self.device_detector_frame.pack(padx=10, pady=10)

        # Create the devices detector object and display it
        self.device_detector = CustomDeviceDetector(self.device_detector_frame, timeout_value=3)

        # Create the device listbox and label
        self.device_listbox = tk.Listbox(self.main_frame)
        self.device_listbox.pack(side=tk.TOP, fill="both", expand=True, padx=10, pady=10)

        self.device_label = tk.Label(self.main_frame, text="Devices")
        self.device_label.pack(side=tk.TOP, padx=10, pady=10)

        # Create the "Show Devices" button
        self.show_devices_button = ttk.Button(self.main_frame, text="Show Devices", command=self.show_devices)
        self.show_devices_button.pack(side=tk.TOP, pady=5)

        def update_devices(self):
        # Clear the device listbox
            self.device_listbox.delete(0, tk.END)

        # Get the list of devices and add their IP addresses to the listbox
        devices = self.devices
        for device in devices:
            self.device_listbox.insert(tk.END, device['ip'])
    
    def create_widgets(self):
        # Create a frame for the main content
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill="both", expand=True)

        # Create the IP address entry widget and add it to the main frame using pack
        self.ip_entry = tk.Entry(self.main_frame)
        self.ip_entry.pack(side=tk.TOP, padx=10, pady=10)

        # Create a frame for the device detector
        self.device_detector_frame = tk.Frame(self.main_frame)
        self.device_detector_frame.pack(padx=10, pady=10)

        # Create the devices detector object and display it
        self.device_detector = CustomDeviceDetector(self.device_detector_frame, timeout_value=3)

        # Create the device listbox and label
        self.device_listbox = tk.Listbox(self.main_frame)
        self.device_listbox.pack(side=tk.TOP, fill="both", expand=True, padx=10, pady=10)

        self.device_label = tk.Label(self.main_frame, text="Devices")
        self.device_label.pack(side=tk.TOP, padx=10, pady=10)

        # Create the "Show Devices" button
        self.show_devices_button = ttk.Button(self.main_frame, text="Show Devices", command=self.show_devices)
        self.show_devices_button.pack(side=tk.TOP, pady=5)

    def show_devices(self):
        # Clear the device listbox
        self.device_listbox.delete(0, tk.END)

        # Get the list of devices and add their IP addresses to the listbox
        devices = self.device_detector.devices
        for device in devices:
            self.device_listbox.insert(tk.END, device['ip'])

if __name__ == "__main__":
    root = Ui_IoTShield(None)
    root.mainloop()