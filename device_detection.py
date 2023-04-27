import ipaddress
import logging
import platform
import re
import socket
import subprocess
import threading
import time
import tkinter as tk
import tkinter.messagebox as messagebox
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from threading import Thread
from tkinter import messagebox, ttk
import json
import netifaces
import nmap
import psutil
import requests
from getmac import get_mac_address

from device_clustering import DeviceClustering

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

class DeviceDetector:
    def __init__(self, parent, num_threads=10):
        super().__init__(parent)
        self.num_threads = num_threads
        self.devices_table = None
        self.progress_bar = None
        self.devices = []  # Add this line

        # Initialize UI
        self.initialize_ui()

    def handle_error(self, title, message):
        self.after(0, messagebox.showerror, title, message)

    def initialize_ui(self):
        # Create the "Scan Devices" button
        scan_button = tk.Button(self, text="Scan Devices", command=self.start_device_scan)
        scan_button.pack(pady=5)

        # Create the devices table
        self.devices_table = tk.Frame(self, bd=1, relief="solid")
        self.devices_table.pack(pady=5)

        # Create the progress bar
        self.progress_bar = ttk.Progressbar(self, orient="horizontal", mode="indeterminate")
        self.progress_bar.pack(pady=5)

    def start_device_scan(self):
        # Start the device scanning process in a separate thread
        scan_thread = Thread(target=self.scan_devices)
        scan_thread.start()

    def scan_devices(self):
        try:
            # Display the progress bar and disable the scan button
            self.progress_bar.start()
            scan_button = self.winfo_children()[0]
            scan_button.configure(state=tk.DISABLED)

            # Get the IP range to scan
            ip_range = self.get_ip_range()

            # Scan the devices in the IP range
            devices = []
            with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
                futures = [executor.submit(self.get_device_info, ip) for ip in ip_range]
                for future in futures:
                    device_info = future.result()
                    if device_info:
                        devices.append(device_info)

            # Store scanned devices in the instance variable
            self.devices = devices

        except Exception as e:
            self.handle_error("Error", f"An error occurred while trying to scan devices: {e}")

        finally:
            # Stop the progress bar and re-enable the scan button
            self.progress_bar.stop()
            scan_button.configure(state=tk.NORMAL)

    def get_devices(self):
        # Implement the logic for fetching devices here
        devices = []  # Replace with the actual list of devices
        return devices

    def get_ip_range(self):
        try:
            local_ip = None
            for addrs in psutil.net_if_addrs().values():
                for addr in addrs:
                    if addr.family == socket.AF_INET:
                        local_ip = addr.address
                        netmask = addr.netmask
                        break

                if local_ip and netmask:
                    break

            if not local_ip or not netmask:
                raise ValueError("Could not find a default gateway to determine the IP range.")

            ip_interface = ipaddress.IPv4Interface(f"{local_ip}/{netmask}")
            ip_network = ip_interface.network
            ip_range = [str(ip) for ip in ip_network.hosts()]

            return ip_range

        except Exception as e:
            logger.error(f"Error while trying to get IP range: {e}")
            raise
 
    def update_devices_table(self, devices):
        for widget in self.devices_table.winfo_children():
            widget.destroy()

        headers = ["Device Name", "IP Address", "MAC Address", "Device Type", "Software Version", "CPU Data", "Memory Data"]
        for i, header in enumerate(headers):
            label = tk.Label(self.devices_table, text=header, font=("Arial", 10, "bold"))
            label.grid(row=0, column=i, padx=5, pady=5)

        for i, device in enumerate(devices, start=1):
            device_name_label = tk.Label(self.devices_table, text=device.get("device_name", "Unknown"))
            device_name_label.grid(row=i, column=0, padx=5, pady=5)

            device_ip_label = tk.Label(self.devices_table, text=device["ip"])
            device_ip_label.grid(row=i, column=1, padx=5, pady=5)

            device_mac_label = tk.Label(self.devices_table, text=device.get("mac", "Unknown"))
            device_mac_label.grid(row=i, column=2, padx=5, pady=5)

            device_type_label = tk.Label(self.devices_table, text=device.get("device_type", "Unknown"))
            device_type_label.grid(row=i, column=3, padx=5, pady=5)

            software_version_label = tk.Label(self.devices_table, text=device.get("software_version", "Unknown"))
            software_version_label.grid(row=i, column=4, padx=5, pady=5)

            cpu_data_label = tk.Label(self.devices_table, text=device.get("cpu_data", "Unknown"))
            cpu_data_label.grid(row=i, column=5, padx=5, pady=5)

            memory_data_label = tk.Label(self.devices_table, text=device.get("memory_data", "Unknown"))
            memory_data_label.grid(row=i, column=6, padx=5, pady=5)

    def get_device_info(self, ip):
        try:
            # Get basic device information
            hostname = socket.getfqdn(ip)
            mac = get_mac_address(ip=ip)

            device_info = {
                "ip": ip,
                "hostname": hostname,
                "mac": mac,
                "device_name": "Unknown",
                "device_type": "Unknown",
                "software_version": "Unknown",
                "cpu_data": "Unknown",
                "memory_data": "Unknown"
            }

            # Get additional device information (e.g., device name, device type, etc.) using requests or other libraries

            # ... (code to fetch additional device information)

            return device_info

        except Exception as e:
            logger.error(f"Error while trying to get device info for IP {ip}: {e}")
            return None

    def get_device_info(self, ip):
        try:
            # Get basic device information
            hostname = socket.getfqdn(ip)
            mac = get_mac_address(ip=ip)

            device_info = {
                "ip": ip,
                "hostname": hostname,
                "mac": mac,
                "device_name": "Unknown",
                "device_type": "Unknown",
                "software_version": "Unknown",
                "cpu_data": "Unknown",
                "memory_data": "Unknown"
            }

            # Get additional device information (e.g., device name, device type, etc.) using requests or other libraries
            try:
                response = requests.get(f"http://example-device-api.com/devices/{ip}/info")
                if response.status_code == 200:
                    device_data = json.loads(response.content)
                    device_info["device_name"] = device_data.get("device_name", "Unknown")
                    device_info["device_type"] = device_data.get("device_type", "Unknown")
                    device_info["software_version"] = device_data.get("software_version", "Unknown")
                    device_info["cpu_data"] = device_data.get("cpu_data", "Unknown")
                    device_info["memory_data"] = device_data.get("memory_data", "Unknown")
                else:
                    logger.warning(f"Unable to fetch additional device info for IP {ip}.")
            except Exception as e:
                logger.warning(f"Error while trying to fetch additional device info for IP {ip}: {e}")

            return device_info

        except Exception as e:
            logger.error(f"Error while trying to get device info for IP {ip}: {e}")
            return None

