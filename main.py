import os
import socket
import sys
import tkinter as tk
from email.message import EmailMessage
from ipaddress import IPv4Address, ip_network
from device_detector import DeviceDetector
import nmap

from device_detection import DeviceDetector
from gui import IoTShieldGUI

class Main(tk.Tk):
    """
    Main class for Device Detector
    """
    def __init__(self):
        super().__init__()
        self.title("Device Detector")
        self.timeout_value = 10
        self.num_threads = 10

        # Instantiate the Gui class
        self.gui = IoTShieldGUI(self)
        self.device_list = []

        # Add GUI elements here
        # Get the IP address range of the current network
        self.device_detector = DeviceDetector(ip_range=self.get_ipv4_network(), device_list=self.device_list)



def get_ipv4_network():
    """
    Get the IP address range of the current network
    :return: str, the IP address range
    """
    try:
        # Get the IP address of the current machine
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]

        # Generate the IP address range for the network
        network = ip_network(ip_address + "/24", strict=False)
        return str(network)
    
    except OSError:
        return "No network connection"



if __name__ == "__main__":
    app = Main()
    app.mainloop()
