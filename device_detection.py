import concurrent.futures
import ipaddress
import logging
import socket
from datetime import datetime
import netifaces
import subprocess
import sys
import threading
import tkinter
import tkinter as tk
import tkinter.ttk as ttk
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

import nmap
import psutil
import requests
from getmac import get_mac_address


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

class DeviceDetector:
    
    def __init__(self, user_agent=None, timeout=1, num_threads=5):
        print("Initializing DeviceDetector")
        self.user_agent = user_agent
        self.timeout = timeout
        self.num_threads = num_threads
        self.local_ip = requests.get('https://api.ipify.org').text
        self.loading_popup = None
        
    def show_loading_popup(self):
        if self.loading_popup is None:
            self.loading_popup = tkinter.Toplevel()
            self.loading_popup.title("Scanning...")

            loading_label = tkinter.Label(
                self.loading_popup, text="Please wait while scanning the network...")
            loading_label.pack(padx=20, pady=20)

        self.loading_popup.lift()
        self.loading_popup.update()
    
    def hide_loading_popup(self):
        if self.loading_popup is not None:
            self.loading_popup.destroy()
            self.loading_popup = None
    
    def get_ip_range(self):
        ip_data = get_ip_data() # Assuming you have a function to get the IP data
        if not ip_data or 'netmask' not in ip_data[0]:
            # Handle the case when the netmask key is not present in the dictionary
            print("Error: Unable to get netmask information")
            return None
        else:
            netmask = ip_data[0]['netmask']

        # Extract the network address from the IP address and netmask
        network_address = '.'.join(str(int(ip) & int(netmask.split('.')[i])) for i, ip in enumerate(ip_data[0]['addr'].split('.')))
        
        # Construct the IP range to scan by combining the network address and the host

        
        return ip_range


    def scan_devices(self):
        devices = []
        ip_range = self.get_ip_range()
        queue = Queue()
        
        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            for ip in ip_range:
                executor.submit(self.scan_device, ip, queue)
                
        while not queue.empty():
            devices.append(queue.get())
                
        return devices
    

class IoTDevice:
    def __init__(self, ip, mac, hostname, dns_data, port_data):
        self.ip = ip
        self.mac = mac
        self.hostname = hostname
        self.dns_data = dns_data
        self.port_data = port_data

    def scan_devices(self):
        devices = []
        ip_range = self.get_ip_range()  # Assuming you have a method to get the IP range to scan
        queue = Queue()
        for _ in range(self.num_threads):
            network_scan_thread = NetworkScanThread(ip_range, queue)
            network_scan_thread.start()
            network_scan_thread.join()
            devices = network_scan_thread.devices

        return devices


    def get_mac_address(self, ip):
        try:
            mac = get_mac_address(ip=ip, timeout=self.timeout)
        except Exception:
            mac = None
        return mac

    def get_device_type(self, mac):
        if mac is None:
            return ""
        else:
            # Implement a function to get the device type based on its MAC address
            return "Unknown"

    def get_last_seen(self, ip):
        """
        Gets the last time a device with the given IP address was seen on the network.
        """
        nm = nmap.PortScanner()
        nm.scan(hosts=ip, arguments='-sP')
        hosts = nm.all_hosts()
        if len(hosts) > 0:
            host = hosts[0]
            last_seen = nm[host]['lastboot']
            return last_seen
        else:
            return "Unknown"

    def close_loading_popup(self):
        self.loading_popup.destroy()

    def get_ip_range(self):
        gateways = netifaces.gateways()
        default_gateway = gateways.get('default', {}).get(netifaces.AF_INET, None)
        if default_gateway:
            iface = default_gateway[1]
            for addr in netifaces.ifaddresses(iface).get(netifaces.AF_INET, []):
                ip = addr['addr']
                netmask = addr['netmask']
                network = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
                ip_range = [str(ip) for ip in network]
                return ip_range
        else:
            raise ValueError("Could not find a default gateway to determine the IP range.")
    

class DeviceIcons:
    def __init__(self):
        self.device_icons = {
            "Computer": "computer_icon.png",
            "Mobile": "mobile_icon.png",
            "CCTV Camera": "cctv_icon.png",
            "Router": "router_icon.png",
            "IP Telephone": "telephone_icon.png",
            "Amazon Echo": "echo_icon.png",
            "Apple Device": "apple_icon.png",
            "Unknown": "default_icon.png"
        }

    def get_device_icon(self, device_type):
        return self.device_icons.get(device_type, "default_icon.png")


class DeviceClustering:
    def __init__(self, devices):
        self.devices = devices
        self.device_types = ["Computer", "Mobile", "CCTV Camera", "Router",
                             "IP Telephone", "Amazon Echo", "Apple Device", "Unknown"]
        self.device_type_icons = DeviceIcons()

    def get_device_types(self):
        return self.device_types

    def get_device_type_icon(self, device_type):
        return self.device_type_icons.get_device_icon(device_type)

    def cluster_devices(self):
        """
        Groups the devices by type.
        """
        clusters = {}
        for device_type in self.device_types:
            clusters[device_type] = []
        for device in self.devices:
            device_type = device["device_type"]
            clusters[device_type].append(device)
        return clusters


class NetworkScanThread(threading.Thread):
    def __init__(self, ip_range, queue):
        threading.Thread.__init__(self)
        self.ip_range = ip_range
        self.queue = queue

    def run(self):
        for ip in self.ip_range:
            device_info = self.get_device_info(ip)
            if device_info:
                self.queue.put(device_info)

    def get_mac_address(self, ip):
        return get_mac_address(ip=ip)

    def get_local_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        except Exception as e:
            logger.error(f"Error getting local IP address: {e}")
            ip = "127.0.0.1"
        finally:
            s.close()
        return ip

    def get_network_prefix(self, local_ip):
        return local_ip.rsplit(".", 1)[0]

    def get_device_info(self, ip):
        mac = self.get_mac_address(ip)
        if mac:
            try:
                hostname = socket.gethostbyaddr(ip)[0]
                dns_data = {'http': f'http://{hostname}', 'https': f'https://{hostname}'}
            except socket.herror:
                hostname = None
                dns_data = {}

            port_data = []
            for port in [80, 443]:  # Add any other ports you want to check
                protocol = 'tcp'
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((ip, port))
                if result == 0:
                    port_data.append({'port': port, 'state': 'open', 'protocol': protocol})
                else:
                    port_data.append({'port': port, 'state': 'closed', 'protocol': protocol})
                sock.close()

            device = IoTDevice(ip, mac, hostname, dns_data, port_data)
            return device

def main():
    detector = DeviceDetector()
    devices = detector.scan_devices()
    print(devices)

if __name__ == "__main__":
    main()