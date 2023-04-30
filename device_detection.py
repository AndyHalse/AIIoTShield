import netifaces
import nmap
import requests
from getmac import get_mac_address
from concurrent.futures import ThreadPoolExecutor
import threading
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import os


class CustomDeviceDetector:
    def __init__(self, parent, num_threads=10, timeout_value=3):
        self.parent = parent
        self.num_threads = num_threads
        self.timeout_value = timeout_value
        self.progress_bar = ttk.Progressbar(
            self.parent, orient=tk.HORIZONTAL, length=200, mode="indeterminate")
        self.running = False
        self.num_threads = num_threads
        self.devices = []
        self.scan_button = tk.Button(
            self.parent, text="Scan Devices", command=self.scan_devices)
        self.running = False
        self.device_name_entry = None
        self.device_ip_label = None
        self.device_ip_entry = None
        self.add_button = None
        self.ip_entry = tk.Entry(self.parent)
        self.devices_table = ttk.Frame(parent, borderwidth=1, relief="solid")

        # Create the widgets
        self.devices_table = tk.Frame(self.parent, bd=1, relief="solid")
        self.devices_table.columnconfigure(0, weight=1)
        self.devices_table.columnconfigure(1, weight=1)

        self.device_label = tk.Label(self.devices_table, text="Devices")

        self.status_label = tk.Label(
            self.devices_table, text="Scanning...", font=("Arial", 16))

        # Start the device scanning process
        self.scan_devices()

    def handle_error(self, title, message):
        def show_error():
            messagebox.showerror(title, message)
        self.parent.after(0, show_error)

    def show_error(error_message):
        def show_error_inner():
            self.handle_error(
                "Error", f"An error occurred while trying to update the devices table: {error_message}")
        self.parent.after(0, show_error_inner)

    def scan_devices(self):
        if self.running:
            return

        self.running = True
        self.progress_bar.start()

        # Call the _scan_devices() function in a separate thread to avoid freezing the UI
        scan_thread = threading.Thread(target=self._scan_devices)
        scan_thread.start()


    def _scan_devices(self):
        try:
            self.devices = self.detect_devices()
            if hasattr(self, "gui"):
                self.gui.devices = self.devices
                self.gui.create_devices_table()
        except Exception as e:
            def show_error(error_message):
                def show_error_inner():
                    self.handle_error(
                        "Error", f"An error occurred while trying to update the devices table: {error_message}")
                self.parent.after(0, show_error_inner)
            show_error(str(e))

    def detect_devices(self):
        # Get a list of IP addresses for all network interfaces
        ip_addresses = []
        for interface in netifaces.interfaces():
            if netifaces.AF_INET in netifaces.ifaddresses(interface):
                addresses = netifaces.ifaddresses(interface)[netifaces.AF_INET]
                for address in addresses:
                    ip_addresses.append(address["addr"])

        # Scan the network for devices
        devices = []
        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            futures = [executor.submit(self.get_device_info, ip_address)
                       for ip_address in ip_addresses]
            for future in futures:
                device = future.result()
                if device is not None:
                    devices.append(device)

        # Return the list of devices
        return devices

    def get_device_info(self, ip_address):
        try:
            # Get the MAC address of the device
            mac_address = get_mac_address(ip=ip_address)

            # Get the device name by sending a request to the device's web server
            url = f"http://{ip_address}/"
            response = requests.get(url, timeout=self.timeout_value)
            device_name = response.headers.get("Server", "Unknown")

            # Determine the type of device
            nm = nmap.PortScanner()
            nm.scan(hosts=ip_address, arguments="-O")
            device_type = nm[ip_address]["osmatch"][0].get("name", "")

            # Check if the device is an Amazon Echo
            if "Amazon" in device_name:
                device_type = "AmazonEcho"

            # Return the device info as a dictionary
            return {
                "ip_address": ip_address,
                "mac_address": mac_address,
                "device_name": device_name,
                "device_type": device_type,
            }

        except Exception:
            return None

    def update_devices_table(self, devices):
        # Clear the table
        for child in self.devices_table.get_children():
            self.devices_table.delete(child)

        # Create the table headers
        device_name_header = tk.Label(self.devices_table, text="Device Name")
        device_name_header.grid(row=0, column=0, sticky="nsew")
        device_ip_header = tk.Label(self.devices_table, text="IP Address")
        device_ip_header.grid(row=0, column=1, sticky="nsew")

        # Add the devices to the table
        for i, device in enumerate(devices):
            device_name = device.get("device_name", "Unknown")
            device_ip = device["ip_address"]

            # Create the device type icon
            device_type = device.get("device_type", "")
            device_icon_file = f"{device_type}.png"
            device_icon = tk.PhotoImage(file=device_icon_file)

            device_label = tk.Label(
                self.devices_table, text=device_name, name=f"device_label_{i}")
            device_label.grid(row=i+1, column=0, sticky="nsew")

            ip_label = tk.Label(self.devices_table, text=device_ip)
            ip_label.grid(row=i+1, column=1, sticky="nsew")

            icon_label = tk.Label(self.devices_table, image=device_icon)
            icon_label.grid(row=i+1, column=2, sticky="nsew")

        # Update the status label
        num_devices = len(devices)
        self.status_label.configure(text=f"{num_devices} devices found")

        # Update the UI
        self.progress_bar.stop()
        self.scan_button.configure(state=tk.NORMAL)
        self.devices_table.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.status_label = tk.Label(
            self.devices_table, text="Scanning...", font=("Arial", 16))
