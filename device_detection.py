import csv
import hashlib
import ipaddress
import os
import socket
import subprocess
from datetime import datetime

import netifaces
import nmap
from nmap import PortScanner
from PIL import Image, ImageTk
from sklearn.cluster import KMeans


class DetectedDevice:
    def __init__(self, ip_address, mac_address, vendor_name, model, cpu_data, memory_data, device_type, dns):
        self.ip_address = ip_address
        self.mac_address = mac_address
        self.vendor_name = vendor_name
        self.model = model
        self.cpu_data = cpu_data
        self.memory_data = memory_data
        self.device_type = device_type
        self.dns = dns

class DeviceDetector:
    def __init__(self, csv_file='unknown_devices.csv'):
        self.csv_file = csv_file
        self.devices = []

    def scan_network(self):
        interfaces = netifaces.interfaces()
        for interface in interfaces:
            addrs = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addrs:
                for link in addrs[netifaces.AF_INET]:
                    ip_addr = link['addr']
                    self.detect_devices(ip_addr)

    def detect_devices(self, ip_addr):
        try:
            hostname = socket.gethostbyaddr(ip_addr)[0]
            if hostname not in ("", "localhost", "localhost.localdomain"):
                self.devices.append((ip_addr, hostname))
        except:
            pass

    def save_devices_csv(self):
        with open(self.csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["IP Address", "Hostname"])
            writer.writerows(self.devices)

    # Function to generate secure logs
    def generate_secure_log(log_file, action):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - {action}\n"

        with open(log_file, "a") as f:
            f.write(log_entry)

        log_hash = hashlib.sha256(log_entry.encode("utf-8")).hexdigest()
        with open(log_file + ".hash", "a") as f:
            f.write(log_hash + "\n")

    # Function to securely log activities
    def log_activity(activity, log_filename):
        log_entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {activity}\n"
        log_entry_hash = hashlib.sha256(log_entry.encode("utf-8")).hexdigest()
        with open(log_filename, "a") as log_file:
            log_file.write(f"{log_entry}{log_entry_hash}\n")
