import ipaddress
import platform
import socket

from getmac import get_mac_address


class DeviceProcessor:
    def __init__(self, ip):
        self.ip = ip
        self.hostname = self.get_hostname()
        self.mac_address = self.get_mac_address()

    def get_hostname(self):
        try:
            hostname = socket.getfqdn(self.ip)
        except socket.herror:
            hostname = ""
        return hostname

    def get_mac_address(self):
        mac = get_mac_address(ip=self.ip)
        return mac

    @staticmethod
    def get_os():
        return platform.system()

    @staticmethod
    def get_chipset():
        if DeviceProcessor.get_os() == "Windows":
            return platform.processor()
        elif DeviceProcessor.get_os() == "Linux":
            return platform.machine()
        else:
            return "Unknown"

    @staticmethod
    def get_system_version():
        return platform.release()

    @staticmethod
    def needs_updating():
        # Implement a function to check if the system needs updating
        return False

    @staticmethod
    def get_device_icon(device_type):
        # Hardcoded icons for each device type
        if device_type == "Computer":
            return "computer_icon.png"
        elif device_type == "Mobile":
            return "mobile_icon.png"
        elif device_type == "IP Camera":
            return "camera_icon.png"
        elif device_type == "Router":
            return "router_icon.png"
        elif device_type == "IP Telephone":
            return "telephone_icon.png"
        elif device_type == "Amazon Echo":
            return "echo_icon.png"
        elif device_type == "Apple TV":
            return "apple_icon.png"
        else:
            return "default_icon.png"

    def get_device_type(self):
        # Implement a function to determine the device type using the IP address
        return "Unknown"

class DataProcessing:
    def get_local_network_prefixes(self, ip_address):
        """
        Given an IP address, returns a list of network prefixes associated with that IP.
        """
        ip_network = ipaddress.IPv4Network(f"{ip_address}/24", False)
        return [{"prefix": str(ip_network), "start": str(ip_network[1]), "end": str(ip_network[-2])}]

    @classmethod
    def get_device_icon(cls, param):
        pass
