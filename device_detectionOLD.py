import csv
import ipaddress
import os
import socket

import nmap
import psutil

class Device:
    def __init__(self, ip_address, mac_address, vendor_name, model, cpu_data, memory_data):
        self.ip_address = ip_address
        self.mac_address = mac_address
        self.vendor_name = vendor_name
        self.model = model
        self.cpu_data = cpu_data
        self.memory_data = memory_data

class DeviceDetector:
    def __init__(self):
        self.csv_file = os.path.join(os.path.dirname(__file__), 'detected_devices.csv')

    def detect(self):
        detected_devices = []
        ip_ranges = self.get_ip_ranges()

        for ip_range in ip_ranges:
            scanner = nmap.PortScanner()
            scanner.scan(hosts=str(ip_range), arguments="-sP")

            # Iterating over the scanned devices and extracting their info
            for device in scanner.all_hosts():
                if scanner[device].get('addresses'):
                    ip_address = device
                    mac_address = scanner[device]['addresses'].get('mac', "")
                    vendor_name = scanner[device]['vendor'].get(mac_address, "")
                    model = 'unknown'
                    cpu_data = self.get_cpu_data()
                    memory_data = self.get_memory_data()

                    device = Device(ip_address, mac_address, vendor_name, model, cpu_data, memory_data)
                    detected_devices.append(device)

                    self.write_csv(device)

        return detected_devices

    def write_csv(self, device):
        with open(self.csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([device.ip_address, device.mac_address, device.vendor_name, device.model])

    def get_cpu_data(self):
        cpu = psutil.cpu_percent()
        return {'usage': cpu}

    def get_memory_data(self):
        virtual_memory = psutil.virtual_memory()
        memory_usage = virtual_memory.total - virtual_memory.available
        return {'usage': memory_usage}

    def get_ip_ranges(self):
        ip_ranges = []

        interfaces = psutil.net_if_addrs()
        for iface_name in interfaces:
            for addr in interfaces[iface_name]:
                if addr.family == socket.AF_INET:
                    ip_network = ipaddress.ip_network(addr.address + '/' + str(addr.netmask), strict=False)
                    ip_ranges.append(ip_network)

        return ip_ranges
