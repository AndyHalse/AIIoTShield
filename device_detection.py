import concurrent.futures
import ipaddress
import socket
import subprocess
import sys
import threading
import tkinter
import tkinter as tk
import tkinter.ttk as ttk
from concurrent.futures import ThreadPoolExecutor
from tkinter import *
from tkinter import messagebox

import nmap
import psutil
import requests
from device_detector import DeviceDetector
from getmac import get_mac_address
from ping3 import ping

from clustering import DeviceClustering
from logging_setup import get_logger

print(sys.path)

logger = get_logger(__name__)
# Get a list of all network interfaces
net_if_addrs = psutil.net_if_addrs()

# Get a list of IP addresses for each network interface
ip_list = []
for interface_name, interface_addresses in net_if_addrs.items():
    for address in interface_addresses:
        if address.family == socket.AF_INET:
            ip_list.append(address.address)

# Create a list of all network prefixes
network_prefixes = []
for ip in ip_list:
    network_prefix = ipaddress.ip_network(ip, strict=False)
    network_prefixes.append(
        str(network_prefix.network_address) + '/' + str(network_prefix.prefixlen))


class DeviceDetector:
    def __init__(self, user_agent=None, timeout=1):
        self.user_agent = user_agent
        self.timeout = timeout
        self.network_prefixes = network_prefixes
        self.local_ip = requests.get('https://api.ipify.org').text

    def scan_devices(self):
        devices = []
        for prefix in self.network_prefixes:
            for host in range(1, 255):
                ip = f"{prefix[:-3]}.{host}"
                if ip == self.local_ip:
                    continue
                device_info = self.get_device_info(ip)
                if device_info is not None:
                    devices.append(device_info)
        return devices

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

    def get_mac_address(self, ip):
        try:
            mac = get_mac_address(ip=ip, timeout=self.timeout)
        except (getmac.GetMacAddressException, getmac.GetMacAddressNetworkException):
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
    def __init__(self, network_prefixes):
        super().__init__()
        self.network_prefixes = network_prefixes
        self.devices = []
        logger.debug("Initializing NetworkScanThread")

    def run(self):
        logger.debug("Starting NetworkScanThread")

        for prefix in self.network_prefixes:
            for host in range(1, 255):
                ip = f"{prefix[:-3]}.{host}"
                if ip == self.local_ip:
                    continue
                device_info = self.get_device_info(ip)
                if device_info is not None:
                    self.devices.append(device_info)

        logger.debug("NetworkScanThread finished")

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
