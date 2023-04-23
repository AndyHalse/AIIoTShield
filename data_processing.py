import ipaddress
import platform
import socket

from getmac import get_mac_address


class DeviceProcessor:
    def __init__(self, ip):
        self.ip = ip
        self.hostname = self.get_hostname()
        self.mac_address = self.get_mac_address()

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
