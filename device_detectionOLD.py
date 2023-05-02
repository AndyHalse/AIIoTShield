import csv
import threading
import requests
import tkinter as tk
import nmap
import platform
import psutil

from tkinter import messagebox, ttk
from scapy.all import srp

class Device:
    def __init__(self, ip_address, mac_address, vendor_name, model, cpu_data, memory_data):
        self.ip_address = ip_address
        self.mac_address = mac_address
        self.vendor_name = vendor_name
        self.model = model
        self.cpu_data = cpu_data
        self.memory_data = memory_data

class DeviceDetector:
    def __init__(self, user_agent):
        self.user_agent = user_agent
        self.devices = []

    def detect(self, ip_range):
        detected_devices = []
        scanner = nmap.PortScanner()
        scanner.scan(hosts=ip_range, arguments='-sP')

        # Iterating over the scanned devices and extracting their info
        for device in scanner.all_hosts():
            if 'mac' in scanner[device]['addresses']:
                ip_address = device
                mac_address = scanner[device]['addresses']['mac']
                vendor_name = scanner[device]['vendor'][mac_address]
                model = 'unknown'
                cpu_data = self.get_cpu_data()
                memory_data = self.get_memory_data()

                device = Device(ip_address, mac_address, vendor_name, model, cpu_data, memory_data)
                detected_devices.append(device)

                self.write_csv(device)
        return detected_devices

    def write_csv(self, device):
        with open('devices.csv', mode='a', newline='') as devices_file:
            writer = csv.writer(devices_file)
            writer.writerow([device.ip_address, device.mac_address, device.vendor_name, device.model, device.cpu_data, device.memory_data])

    def get_vendor(self, mac_address):
        if mac_address is None:
            return ""

        try:
            response = requests.get(f"https://api.macvendors.com/{mac_address}")
            if response.status_code == 200:
                return response.text.strip()

            return ""
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return ""

    def get_cpu_data(self):
        cpu = platform.processor()
        return cpu

    def get_memory_data(self):
        virtual_mem = psutil.virtual_memory().total
        return virtual_mem