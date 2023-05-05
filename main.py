import socket
import tkinter as tk
from email.message import EmailMessage
from ipaddress import ip_network

from gui import IoTShieldGUI
from device_detector import DeviceDetector

class Main(tk.Tk):
    """
    Main class for Device Detector
    """

    def __init__(self):
        super().__init__()
        self.title("Device Detector")

        # set up a default IP address range
        network = ip_network("192.168.0.0/24", strict=False)

        try:
            # Get the IP address of the current machine
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 53))
                ip_address = s.getsockname()[0]

            # Generate the IP address range for the network
            network = ip_network(ip_address + "/24", strict=False)

        except OSError:
            print("No network connection, defaulting to 192.168.0.0/24")

        # Instantiate the Gui class, and pass the DeviceDetector object as a parameter
        self.device_detector = DeviceDetector(network)
        self.gui = IoTShieldGUI(self, self.device_detector)

if __name__ == "__main__":
    app = Main()
    app.mainloop()
