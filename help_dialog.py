import tkinter as tk

class HelpWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("IoTShield Help")
        self.geometry("600x400")

        # Create the help text
        help_text = """
IoTShield Help

Overview

IoTShield is an application designed to automatically detect and identify all LAN/WAN network devices, including IoT, IP CCTV cameras, routers, IP telephones, wireless mobiles, Amazon 'Echo' devices, Apple Not devices, and any wireless devices that could be vulnerable to outside hackers. The application provides a GUI that displays all devices with their relevant detected device type icon image in an expanding grid fashion along with their IP address, device name, device type, device software/firmware version number, MAC address, CPU data, memory data, and any other relevant information.

How to Use

When you launch IoTShield, it will start scanning the network and display the devices it finds in the GUI. You can click on each device to view more details about it.

Troubleshooting

If you encounter any issues while using IoTShield, please refer to the following troubleshooting tips:

- If you are not seeing any devices in the GUI, make sure that IoTShield is running on the same network as the devices you are trying to detect.
- If you are seeing devices in the GUI but they are not being detected correctly, make sure that the devices are properly connected to the network and are using the correct IP address.
- If you encounter any error messages, please take note of the message and contact the support team for assistance.

Support

If you need any help or have any questions about IoTShield, please contact the support team at support@aiiotshield.com.

Source Code

The source code for IoTShield is available on GitHub at the following link:

https://github.com/AndyHalse/AIIoTShield
        """

        # Create the help text widget
        self.help_text = tk.Text(self, wrap=tk.WORD, state=tk.READONLY)
        self.help_text.insert(tk.END, help_text)

