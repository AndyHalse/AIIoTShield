import concurrent.futures
import ipaddress
import logging
import socket
import subprocess
import sys
import threading
import tkinter
import tkinter as tk
import tkinter.ttk as ttk
from concurrent.futures import ThreadPoolExecutor

import nmap
import psutil
import requests
from device_detector import DeviceDetector
from getmac import get_mac_address

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


class DeviceDetector:
    def __init__(self, user_agent=None, timeout=1):
        print("Initializing DeviceDetector")
        self.user_agent = user_agent
        self.timeout = timeout
        self.local_ip = requests.get('https://api.ipify.org').text

    def show_loading_popup(self):
        self.loading_popup = tkinter.Toplevel()
        self.loading_popup.title("Scanning...")

        loading_label = tkinter.Label(
            self.loading_popup, text="Please wait while scanning the network...")
        loading_label.pack(padx=20, pady=20)

        self.loading_popup.lift()
        self.loading_popup.update()

    def scan_devices(self):
        self.show_loading_popup()

        network_scan_thread = NetworkScanThread()
        network_scan_thread.start()
        network_scan_thread.join()

        devices = network_scan_thread.devices

        self.close_loading_popup()

        return devices

    def get_device_info(self, ip):
        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except (socket.herror, socket.timeout, socket.gaierror):
            hostname = ""

        mac = self.get_mac_address(ip)
        if mac is None:
            return None

        device_type = self.get_device_type(mac)
        last_seen = self.get_last_seen(ip)
        return {"ip": ip, "hostname": hostname, "mac": mac, "device_type": device_type, "last_seen": last_seen}

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
    def __init__(self):
        super().__init__()
        self.devices = []
        logger.debug("Initializing NetworkScanThread")

    def run(self):
        logger.debug("Starting NetworkScanThread")

        local_ip = self.get_local_ip_address()
        network_prefix = self.get_network_prefix(local_ip)

        for host in range(1, 255):
            ip = f"{network_prefix}.{host}"
            if ip == local_ip:
                continue
            device_info = self.get_device_info(ip)
            if device_info is not None:
                self.devices.append(device_info)

        logger.debug("NetworkScanThread finished")

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
        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except (socket.herror, socket.timeout):
            hostname = ""

        mac = self.get_mac_address(ip)
        if mac is None:
            return None

        device_type = self.get_device_type(mac)
        last_seen = self.get_last_seen(ip)
        return {"ip": ip, "hostname": hostname, "mac": mac, "device_type": device_type, "last_seen": last_seen}

    def main():
        detector = DeviceDetector()
        devices = detector.scan_devices()
        print(devices)

if __name__ == "__main__":
    main()

