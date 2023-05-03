import os
import sys
import tkinter as tk
from ipaddress import ip_network
from device_detection import check_compatibility, run_nmap, parse_nmap_output, detect_device_type, detect_ip_ranges, calculate_byte_rates, train_clustering_model, detect_anomalies

class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Device Detector")
        timeout_value = 10
        num_threads = 10
        
        # Add GUI elements here
        self.ip_range_label = tk.Label(text="Enter the IP address range (CIDR notation)")
        self.ip_range_label.pack()
        self.ip_range_entry = tk.Entry()
        self.ip_range_entry.pack()
        
        # Define a button to run device detection
        self.detect_button = tk.Button(text="Detect Devices", command=self.detect_devices)
        self.detect_button.pack()

    def run_device_detection(self, ip_range):
        if not check_compatibility():
            sys.exit("Incompatible OS or chipset")

        nmap_output = run_nmap(ip_range)
        devices = parse_nmap_output(nmap_output)

        for device in devices:
            device["type"] = detect_device_type(device["name"])

        ip_ranges = detect_ip_ranges(devices)

        byte_rates_data = []
        for device in devices:
            byte_rate = calculate_byte_rates([device])[device["ip"]]
            byte_rates_data.append([byte_rate["in"], byte_rate["out"]])

        kmeans = train_clustering_model(byte_rates_data)
        labels = kmeans.predict(byte_rates_data)
        anomalies = detect_anomalies(devices, labels)

        return anomalies

    def detect_devices(self):
        ip_range = self.ip_range_entry.get()
        anomalies = self.run_device_detection(ip_range)
        # Process the anomalies
        
if __name__ == "__main__":
    app = Main()
    app.mainloop()
