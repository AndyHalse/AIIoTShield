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
    def __init__(self, num_threads=10):
        self.num_threads = num_threads

    def get_device_info(self, ip):

cclass DeviceDetectorFrame(tk.Frame):
    def __init__(self, parent, num_threads=10):
        super().__init__(parent)
        self.num_threads = num_threads
        self.devices_table = None
        self.progress_bar = None

        # Initialize UI
        self.initialize_ui()

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

    def show_loading_popup(self):
        loading_popup = tk.Toplevel(self)
        loading_popup.title("Loading")
        loading_popup.geometry("600x300")
        loading_label = tk.Label(loading_popup, text="Scanning devices, please wait...")
        loading_label.pack(expand=True, fill="both")
        loading_popup.lift()
        loading_popup.grab_set()
        self.after(100, lambda: self.scan_devices(loading_popup.destroy))

    def scan_devices(self, destroy_loading_popup=None):
        try:
            if destroy_loading_popup:
                destroy_loading_popup()

            # Display the progress bar and disable the scan button
            self.progress_bar.start()
            scan_button = self.winfo_children()[0]
            scan_button.configure(state=tk.DISABLED)

            # Get the IP range to scan
            ip_range = self.get_ip_range()

            # Scan the devices in the IP range
            devices = []
            with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
                for ip in ip_range:
                    executor.submit(self.get_device_info, ip, devices)

            # Update the devices table
            self.update_devices_table(devices)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while trying to scan devices: {e}")

        finally:
            # Stop the progress bar and re-enable the scan button
            self.progress_bar.stop()
            scan_button.configure(state=tk.NORMAL)
   
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

    def show_loading_popup(self):
        loading_popup = tk.Toplevel(self)
        loading_popup.title("Loading")
        loading_popup.geometry("600x300")
        loading_label = tk.Label(loading_popup, text="Scanning devices, please wait...")
        loading_label.pack(expand=True, fill="both")
        loading_popup.lift()
        loading_popup.grab_set()
        self.after(100, lambda: self.scan_devices(loading_popup.destroy))

    def scan_devices(self, destroy_loading_popup):
        try:
            destroy_loading_popup()
            ip_range = self.get_ip_range()

            def scan():
                while any(executor._threads):
                    self.progress_bar.step(10)
                    self.progress_bar.update()
                    time.sleep(0.1)

            def worker():
                while not queue.empty():
                    ip = queue.get()
                    device_info = self.get_device_info(ip)
                    if device_info:
                        devices.append(device_info)

            queue = Queue()
            devices = []
            for ip in ip_range:
                queue.put(ip)

            with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
                for _ in range(self.num_threads):
                    executor.submit(worker)
                scan_thread = Thread(target=scan)
                scan_thread.start()

        except Exception as e:
            logger.error(f"Error while trying to scan devices: {e}")
            messagebox.showerror("Error", "An error occurred while trying to scan devices.")

        # Add devices to the table
        for i, device in enumerate(devices):
            device_name_label = tk.Label(self.devices_table, text=device["device_type"])
            device_name_label.grid(row=i, column=0, sticky="W")

            device_ip_label = tk.Label(self.devices_table, text=device["ip"])
            device_ip_label.grid(row=i, column=1, sticky="W")

        self.progress_bar.stop()
        self.progress_bar.destroy()

        return devices




    def get_last_seen(self, ip):
        """
        Gets the last time a device with the given IP address was seen on the network.
        """
        nm = nmap.PortScanner()
        nm.scan(hosts=ip, arguments='-sn')
        hosts = nm.all_hosts()
        if len(hosts) > 0:
            host = hosts[0]
            last_seen = nm[host]['lastboot']
            return last_seen
        else:
            return "Unknown"

    def get_device_info(self, ip):
        try:
            response = requests.get(f"http://{ip}", headers={"User-Agent": self.user_agent}, timeout=self.timeout)
            if response.status_code == 200:
                device_type = response.headers.get("Server", "Unknown")
                device_info = {"device_type": device_type, "ip": ip, "last_seen": self.get_last_seen(ip)}
                return device_info
        except requests.exceptions.RequestException:
            pass  # Ignore timeouts and other request exceptions
        return None
