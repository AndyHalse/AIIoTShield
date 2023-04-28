import errno
import ipaddress
import json
import logging
import socket
import threading
import time
import tkinter as tk
import tkinter.messagebox as messagebox
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from threading import Thread
from tkinter import messagebox, ttk

import netifaces
import nmap
import requests
from getmac import get_mac_address

from device_clustering import DeviceClustering

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

class CustomDeviceDetector:
    def __init__(self, parent, timeout_value=3, num_threads=5):
        self.parent = parent
        self.timeout_value = timeout_value
        self.num_threads = num_threads
        self.devices = []
        self.scan_button = None
        self.running = False
        self.device_name_entry = None
        self.device_ip_label = None
        self.device_ip_entry = None
        self.add_button = None
        self.initialize()
        self.ip_entry = tk.Entry(self)

        # Create the widgets
        self.devices_table = tk.Frame(self.parent, bd=1, relief="solid")
    #     self.devices_table.pack(row=1, column=0, sticky=tk.NSEW)
        self.devices_table.columnconfigure(0, weight=1)
        self.devices_table.columnconfigure(1, weight=1)

        self.device_label = tk.Label(self.devices_table, text="Devices")
    #     self.device_label.pack(row=0, column=0, padx=5, pady=5)

        self.status_label = tk.Label(self.devices_table, text="Scanning...", font=("Arial", 16))
    #     self.status_label.pack(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # Start the device scanning process
        self.scan_devices()

    def stop(self):
        self._stop_event.set()

    def _scan_devices(self):
        self.devices = []
        subnet = '.'.join(socket.gethostbyname_ex(socket.gethostname())[2][0].split('.')[0:3]) + '.'
        for i in range(1, 255):
            if self._stop_event.is_set():
                break

            ip = subnet + str(i)
            if ip != socket.gethostbyname(socket.gethostname()):
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(self.timeout_value)
                    s.connect((ip, 135))
                    s.close()
                    self.devices.append({'ip': ip})
                except socket.error as e:
                    if e.errno != errno.ECONNREFUSED:
                        pass
                except socket.timeout:
                    pass

        # Display the found devices
        self.parent.update_devices()

    def run(self):
        self._scan_devices()

    def initialize(self):
        self.create_labels()
        self.create_entry_fields()
        self.create_add_button()

        # Create the listbox for devices
        self.create_listbox()

        # Create the progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_var.set(0)
        self.progress_bar = ttk.Progressbar(self.parent, orient="horizontal", mode="indeterminate", variable=self.progress_var)
        self.progress_bar.pack(row=2, column=0, pady=5)

    def create_labels(self):
        self.device_name_label = tk.Label(self.parent, text="Device Name")
        self.device_name_label.pack(row=3, column=0, padx=5, pady=5)
        self.device_ip_label = tk.Label(self.parent, text="Device IP")
        self.device_ip_label.pack(row=4, column=0, padx=5, pady=5)

    def create_entry_fields(self):
        self.device_name_entry = tk.Entry(self.parent)
        self.device_name_entry.pack(row=3, column=1, padx=5, pady=5)
        self.device_ip_entry = tk.Entry(self.parent)
        self.device_ip_entry.pack(row=4, column=1, padx=5, pady=5)
        self.ip_entry_var = tk.StringVar()
        self.ip_entry = tk.Entry(self.parent, textvariable=self.ip_entry_var)
        self.ip_entry_var.set("Enter IP address...")
        self.ip_entry.bind('<FocusIn>', self.on_entry_click)
        self.ip_entry.bind('<FocusOut>', self.on_focusout)
        self.ip_entry.pack(row=5, column=1, padx=5, pady=5)
        self.port_entry = tk.Entry(self.parent)
        self.port_entry.pack(row=6, column=1, padx=5, pady=5)
        self.add_button = tk.Button(self.parent, text="Add", command=self.add_device)
        self.add_button.pack(row=7, column=1, padx=5, pady=5)

    def on_entry_click(self, event):
        """function that gets called whenever entry is clicked"""
        if self.ip_entry_var.get() == 'Enter IP address...':
            self.ip_entry_var.set('')

    def on_focusout(self, event):
        """function that gets called whenever entry is clicked"""
        if self.ip_entry_var.get() == '':
            self.ip_entry_var.set('Enter IP address...')

    def create_add_button(self):
        self.add_button = tk.Button(self.parent, text="Add", command=self.add_device)
        self.add_button.pack(row=5, column=1, padx=5, pady=5)

    def add_device(self):
        device_name = self.device_name_entry.get()
        device_ip = self.device_ip_entry.get()
        # do something with the device name and ip here

    def create_listbox(self):
        # create the devices table
        self.devices_table = tk.Frame(self.parent, bd=1, relief="solid")
        self.devices_table.pack(row=0, column=0, pady=5)

        self.devices_table.columnconfigure(0, weight=1)
        self.devices_table.columnconfigure(1, weight=1)
        self.devices_table.columnconfigure(2, weight=1)

        # create the listbox for devices
        self.device_listbox = tk.Listbox(self.devices_table, height=10)
        self.device_listbox.pack(row=1, column=0, sticky="nsew", padx=10, pady=10)



    def handle_error(self, title, message):
        self.after(0, messagebox.showerror, title, message)


    def scan_devices(self):
        self.progress_bar.start()

        def _scan_devices():

            # Get all network interfaces and their IP addresses
            interfaces = netifaces.interfaces()
            ip_addresses = []
            for interface in interfaces:
                addresses = netifaces.ifaddresses(interface)
                ip_addresses.extend([addr['addr'] for addr in addresses.get(netifaces.AF_INET, [])])

            # Scan the devices for each IP address
            devices = []
            with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
                futures = [executor.submit(self.get_device_info, ip) for ip in ip_addresses]
                for future in futures:
                    device_info = future.result()
                    if device_info:
                        devices.append(device_info)

            # Store scanned devices in the instance variable
            self.devices = devices

            # Update the devices table
            self.update_devices_table(devices)

            # Re-enable the scan button
            scan_button.configure(state=tk.NORMAL)

        try:
            # Call the _scan_devices() function in a separate thread to avoid freezing the UI
            scan_thread = Thread(target=_scan_devices)
            scan_thread.start()

        except Exception as e:
            self.handle_error("Error", f"An error occurred while trying to scan devices: {e}")

        finally:
            # Stop the progress bar
            self.progress_bar.stop()


    def get_ip_range(self):
        try:
            ipv4_interfaces = [i for i in netifaces.interfaces() if netifaces.AF_INET in netifaces.ifaddresses(i)]
            ip_net_pairs = []
            for i in ipv4_interfaces:
                try:
                    address_info = netifaces.ifaddresses(i)[netifaces.AF_INET][0]
                    ip_net_pairs.append((address_info['addr'], address_info.get('netmask')))
                except KeyError:
                    logger.warning(f"No netmask found for interface {i}. Skipping.")
            ip_range = set()
            for ip_net_pair in ip_net_pairs:
                ip, netmask = ip_net_pair
                if netmask:
                    ip_interface = ipaddress.IPv4Interface(f"{ip}/{netmask}")
                    ip_network = ip_interface.network
                    ip_range.update([str(ip) for ip in ip_network.hosts()])
            return ip_range
        except Exception as e:
            logger.error(f"Error while trying to get IP range: {e}")
            raise


    def update_devices_table(self, devices):
        # Clear the previous content of the devices table
        for widget in self.devices_table.winfo_children():
            widget.destroy()

        # Add the column headers
        tk.Label(self.devices_table, text="IP Address").pack(row=0, column=0, padx=5, pady=5)
        tk.Label(self.devices_table, text="Hostname").pack(row=0, column=1, padx=5, pady=5)
        tk.Label(self.devices_table, text="MAC Address").pack(row=0, column=2, padx=5, pady=5)

        # Add the devices to the table
        for index, device in enumerate(devices):
            ip_address = device.get("ip_address")
            hostname = device.get("hostname", "")
            mac_address = device.get("mac_address", "")

            tk.Label(self.devices_table, text=ip_address).pack(row=index+1, column=0, padx=5, pady=5)
            tk.Label(self.devices_table, text=hostname).pack(row=index+1, column=1, padx=5, pady=5)
            tk.Label(self.devices_table, text=mac_address).pack(row=index+1, column=2, padx=5, pady=5)

    def get_device_info(self, ip):
        try:
            # Get basic device information
            hostname = socket.getfqdn(ip)
            mac = get_mac_address(ip=ip)

            device_info = {
                "ip_address": ip,
                "hostname": hostname,
                "mac_address": mac,
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
