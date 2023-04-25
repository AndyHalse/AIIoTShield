import ipaddress
import logging
import platform
import socket
import threading
import tkinter as tk
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

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


class DeviceDetector(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.timeout = timeout
        self.num_threads = num_threads
        self.devices_table = tk.Frame(self)
        self.devices_table.pack(side="top", fill="both", expand=True)
        self.os_name = platform.system()
        self.os_version = platform.version()
        self.machine_architecture = platform.machine()
        self.processor_name = platform.processor()
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"

    def get_ip_range(self, concurrent=None):
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
        except socket.gaierror:
            # Handle situation where an IPv4 address cannot be found
            print("Could not find IPv4 address, trying alternative method...")
            ip_list = []
            for i in range(256):
                for j in range(256):
                    ip = f"192.168.{i}.{j}"
                    ip_list.append(ip)
            reachable_ips = []
            with concurrent.futures.ThreadPoolExecutor() as executor:
                results = [executor.submit(self.is_ip_reachable, ip) for ip in ip_list]
                for future in concurrent.futures.as_completed(results):
                    if future.result():
                        reachable_ips.append(future.result())
            if len(reachable_ips) == 0:
                raise ValueError("Could not determine IP range.")
            else:
                first_ip = min(reachable_ips)
                last_ip = max(reachable_ips)
                return f"{first_ip}-{last_ip}"
        else:
            ip_parts = local_ip.split('.')
            ip_parts[-1] = '0/24'
            ip_range = '.'.join(ip_parts)
            return ip_range

    def is_ip_reachable(self, ip):
        try:
            socket.setdefaulttimeout(1)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((ip, 80))
            return True
        except OSError:
            return False


    def scan_devices(self):
        # Scan the network for devices
        devices = []

        # Add devices to the table
        for i, device in enumerate(devices):
            device_name_label = tk.Label(self.devices_table, text=device["name"])
            device_name_label.grid(row=i, column=0, sticky="W")

            device_ip_label = tk.Label(self.devices_table, text=device["ip"])
            device_ip_label.grid(row=i, column=1, sticky="W")

        return devices

    def scan_device(self, ip, queue):
        mac = self.get_mac_address(ip)
        device_manufacturer = self.get_device_manufacturer(mac)
        device_type = self.get_device_type(device_manufacturer)

        last_seen = self.get_last_seen(ip)
        device_info = {'ip': ip, 'mac': mac, 'device_type': device_type, 'last_seen': last_seen}
        queue.put(device_info)


    def get_device_info(self, ip):
        mac = self.get_mac_address(ip)
        device_manufacturer = self.get_device_manufacturer(mac)
        device_type = self.get_device_type(device_manufacturer)
        last_seen = self.get_last_seen(ip)
        return {'ip': ip, 'mac': mac, 'device_type': device_type, 'last_seen': last_seen}

    def get_mac_address(self, ip):

        if self.os_name == 'Windows':
            return self.get_mac_address_windows(ip)
        elif self.os_name == 'Linux':
            return self.get_mac_address_linux(ip)
        else:
            return None

    def get_mac_address_windows(self, ip, subprocess=None, re=None):
        """
        Returns the MAC address of the device with the given IP address on Windows.
        """
        command = f"arp -a {ip}"
        output = subprocess.check_output(command, shell=True).decode("utf-8")
        mac_address = re.search(r"(([0-9A-Fa-f]{2}-){5}[0-9A-Fa-f]{2})", output)
        if mac_address:
            return mac_address.group(0)
        else:
            return None

    def get_mac_address_linux(self, ip, subprocess=None, re=None):
        """
        Returns the MAC address of the device with the given IP address on Linux.
        """
        command = f"arp {ip}"
        output = subprocess.check_output(command, shell=True).decode("utf-8")
        mac_address = re.search(r"(([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2})", output)
        if mac_address:
            return mac_address.group(0)
        else:
            return None

    def get_device_manufacturer(self, mac, re=None, urllib=None):
        """
        Returns the manufacturer of the device with the given MAC address.
        """
        if mac is None:
            return None

        # Get the first 3 octets of the MAC address
        mac_prefix = mac.split(':')[0] + ':' + mac.split(':')[1] + ':' + mac.split(':')[2]

        # Load the OUI data from the IEEE website
        try:
            with urllib.request.urlopen("http://standards-oui.ieee.org/oui.txt") as response:
                html = response.read().decode('utf-8')
                oui_list = re.findall(r"([0-9A-Fa-f]{2}-[0-9A-Fa-f]{2}-[0-9A-Fa-f]{2})\s+\(hex\)\s+(.+)", html)
                oui_dict = {key: value for key, value in oui_list}
        except:
            # Handle situation where OUI data cannot be retrieved
            return None

        # Find the manufacturer for the given MAC prefix
        manufacturer = oui_dict.get(mac_prefix)
        return manufacturer

    def get_device_type(self, device_manufacturer):
        """
        Returns the type of device based on the manufacturer.
        """
        if device_manufacturer is None:
            return None

        device_type_dict = {
            'Apple, Inc.': 'iPhone',
            'Samsung Electronics Co.': 'Samsung Galaxy',
            'Xiaomi Communications Co.': 'Xiaomi Phone',
            'Huawei Technologies Co.': 'Huawei Phone',
            'Microsoft Corporation': 'Microsoft Surface',
            'Dell Inc.': 'Dell Computer',
            'Hewlett Packard': 'HP Computer'
        }

        for key in device_type_dict:
            if key in device_manufacturer:
                return device_type_dict[key]

        return None


class IoTDevice:
    def __init__(self, ip, mac, hostname, dns_data, port_data):
        self.num_threads = None
        self.ip = ip
        self.mac = mac
        self.hostname = hostname
        self.dns_data = dns_data
        self.port_data = port_data

    def scan_devices(self):
        devices = []
        ip_range = self.get_ip_range()
        queue = Queue()
        for _ in range(self.num_threads):
            network_scan_thread = NetworkScanThread(ip_range, queue)
            network_scan_thread.start()
            network_scan_thread.join()
            devices = network_scan_thread.devices

        return devices

    def get_mac_address(self, ip, url=None):
        try:
            response = requests.get(url)
            vendor = response.text.strip()
        except:
            vendor = None
            logger.error(f"Failed to retrieve vendor for MAC address {self.mac}.")

        return self.mac

    def get_device_type(self, mac):
        if mac is None:
            return ""
        else:
            # Get the device vendor using the MAC address OUI lookup API
            url = f"https://api.macvendors.com/{mac}"
            try:
                response = requests.get(url)
                vendor = response.text.strip()
            except:
                vendor = None
                logger.error(f"Failed to retrieve vendor for MAC address {mac}.")

            # Map the vendor name to a device type (you can modify or add to this dictionary as needed)
            device_types = {
                "Apple": "Apple Device",
                "Samsung": "Mobile",
                "Microsoft": "Computer",
                "Dell": "Computer",
                "HP": "Computer",
                "Lenovo": "Computer",
                "Cisco": "Router",
                "Unknown": "Unknown"
            }
            device_type = device_types.get(vendor, "Unknown")
            return device_type

    def get_device_manufacturer(self, mac):
        if mac is None:
            return ""
        else:
            # Get the device vendor using the MAC address OUI lookup API
            url = f"https://api.macvendors.com/{mac}"
            try:
                response = requests.get(url)
                vendor = response.text.strip()
            except:
                vendor = None
            return vendor

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

        clusters = {}
        for device_type in self.device_types:
            clusters[device_type] = []
        for device in self.devices:
            device_type = device["device_type"]
            clusters[device_type].append(device)
        return clusters

class NetworkScanner:
    def __init__(self):
        self.nm = nmap.PortScanner()
        pass
    def scan_devices(self):
        self.nm.scan(hosts='192.168.1.0/24', arguments='-n -sP -PE -PA21,23,80,3389')
        hosts = [(x, self.nm[x]['status']['state']) for x in self.nm.all_hosts()]
        for host, status in hosts:
            print(f"{host}: {status}")
        pass

class NetworkScanThread(threading.Thread):
    def __init__(self, ip_range, queue):
        threading.Thread.__init__(self)
        self.devices = None
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
        device_manufacturer = self.get_device_manufacturer(mac)
        device_type = self.get_device_type(device_manufacturer)
        last_seen = self.get_last_seen(ip)
        return {'ip': ip, 'mac': mac, 'device_type': device_type, 'last_seen': last_seen}

    def get_mac_address(self, ip):
        pass

    def get_device_manufacturer(self, mac):
        pass

    def get_device_type(self, device_manufacturer):
        pass

    def get_last_seen(self, ip):
        pass