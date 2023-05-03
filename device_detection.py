import csv
import hashlib
import os
import platform
import random
import smtplib
import subprocess
import sys
import pandas as pd
import tkinter as tk
import nmap
import psutil

from datetime import datetime
from email.message import EmailMessage
from io import BytesIO
from fpdf import FPDF
from PIL import Image, ImageTk
from sklearn.cluster import KMeans
from ipaddress import ip_network, ip_interface


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

    @staticmethod
    def check_compatibility():
        """Checks if the operating system and processor architecture are compatible with the software
        Returns:
            bool: True if macOS (Darwin), Linux, or Windows and processor made by Apple, AMD, or Intel, False otherwise
        """
        os = platform.system()
        processor = platform.processor()

        if os == "Darwin" and ("Apple" in processor or "Intel" in processor):
            return True
        elif os == "Linux" and ("AMD" in processor or "Intel" in processor):
            return True
        elif os.startswith("Windows") and ("AMD" in processor or "Intel" in processor):
            return True
        else:
            return False

    # Function to ping IP addresses
    def ping_ip(self, ip):
        param = "-n" if platform.system().lower() == "windows" else "-c"
        command = ["ping", param, "1", ip]
        return subprocess.call(command) == 0

    # Function to run nmap for device discovery
    def run_nmap(self, ip_range):
        nmap_cmd = f"nmap -sn {ip_range}"
        nmap_output = subprocess.check_output(nmap_cmd, shell=True).decode("utf-8")
        return nmap_output

    # Function to parse nmap output
    def parse_nmap_output(self, nmap_output):
        devices = []
        lines = nmap_output.split("\n")
        for i, line in enumerate(lines):
            if "Nmap scan report for" in line:
                device = {}
                device["ip"] = line.split()[-1]
                device["name"] = lines[i + 1].split()[-1] if "Host is up" in lines[i + 1] else ""
                devices.append(device)
        return devices

        # Function to get device icons

    def get_device_icon(self, device_type):
                icons = {
                    "cctv": "cctv_icon.png",
                    "echo": "echo_icon.png",
                    "apple_iot": "apple_iot_icon.png",
                    "unknown": "unknown_icon.png",
                }
                return icons.get(device_type, "unknown_icon.png")

    def detect_devices(self):
                ip_range = None
                for interface in psutil.net_if_addrs():
                    if interface.startswith('en') or interface.startswith('eth'):
                        for snic in psutil.net_if_addrs()[interface]:
                            if snic.family == 2:
                                ip_address = snic.address
                                ip_network_str = f"{ip_address}/24"
                                for ip in ip_network(ip_network_str).hosts():
                                    if ip != ip_address:
                                        if self.ping_ip(str(ip)):
                                            ip_range = f"{ip_address.split('.')[0]}.{ip_address.split('.')[1]}.0/24"
                                            break
                                break
                if ip_range is None:
                    return

                nmap_output = self.run_nmap(ip_range)

                devices = self.parse_nmap_output(nmap_output)

                known_devices_df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'known_devices.csv'))

                unknown_devices = []

                for device in devices:
                    mac_address = self.get_mac_address(device['ip'])
                    vendor_name, model = self.identify_device(mac_address, known_devices_df)
                    cpu_data = self.get_cpu_data(device['ip'])
                    memory_data = self.get_memory_data(device['ip'])
                    device_type = self.identify_device_type(vendor_name, model)
                    device_icon = self.get_device_icon(device_type)
                    if vendor_name == 'Unknown':
                        unknown_devices.append(Device(device['ip'], mac_address, vendor_name, model, cpu_data, memory_data))
                    else:
                        print(f"{device['ip']} is a {vendor_name} {model} device")
                        image = Image.open(device_icon)
                        image.show()        

        # Function to save unknown devices to CSV
    def save_unknown_devices(self, unknown_devices):
                if len(unknown_devices) == 0:
                    return

                with open(self.csv_file, 'a', newline='') as file:
                    writer = csv.writer(file)
                    for device in unknown_devices:
                        writer.writerow([device.ip_address, device.mac_address, device.vendor_name, device.model, device.cpu_data, device.memory_data])

        
        # Function to get CPU data for detected device
    def get_cpu_data(self, ip_address):
        cpu_data = {}
        ssh = self.connect_to_device(ip_address, 'root', 'password')
        if ssh is not None:
            stdin, stdout, stderr = ssh.exec_command('cat /proc/cpuinfo')
            cpu_info = stdout.read().decode()
            for line in cpu_info.split("\n"):
                if "processor" in line:
                    cpu_data["processor_count"] = cpu_data.get("processor_count", 0) + 1
                elif "model name" in line:
                    cpu_data["model_name"] = line.split(":")[1].strip()
            ssh.close()
        return cpu_data

    # Function to get memory data for detected device
    def get_memory_data(self, ip_address):
        memory_data = {}
        ssh = self.connect_to_device(ip_address, 'root', 'password')
        if ssh is not None:
            stdin, stdout, stderr = ssh.exec_command('free -m')
            memory_info = stdout.read().decode()
            for line in memory_info.split("\n"):
                if "Mem" in line:
                    parts = line.split()
                    memory_data["total"] = parts[1]
                    memory_data["used"] = parts[2]
                    memory_data["free"] = parts[3]
                    break
            ssh.close()
        return memory_data        

    def identify_device_type(self, vendor_name, model, ip_address):
        ssh = self.connect_to_device(ip_address, 'root', 'password')
        device_type = None
        if ssh is not None:
            if vendor_name is not None:
                if 'cisco' in vendor_name.lower():
                    device_type = 'cisco'
                elif 'juniper' in vendor_name.lower():
                    device_type = 'juniper'
                elif 'dell' in vendor_name.lower():
                    device_type = 'dell'
            ssh.close()
        return device_type


    # Function to calculate byte rates
    def calculate_byte_rates(self, devices):
        byte_rates = {}
        for device in devices:
            byte_rates[device["ip"]] = {"in": random.randint(
                1000, 10000), "out": random.randint(1000, 10000)}
        return byte_rates

    def detect_anomalies(devices, byte_rates):
        # Perform anomaly detection on byte_rates data
        anomalies = []

        # Assume anomalies are detected for any devices with byte rates above a certain threshold
        for i, device in enumerate(devices):
            if byte_rates[device["ip"]]["in"] > 10000 or byte_rates[device["ip"]]["out"] > 10000:
                anomalies.append(i)

        return anomalies

    # Function to generate secure logs
    def generate_secure_log(log_file, action):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - {action}\n"

        with open(log_file, "a") as f:
            f.write(log_entry)

        log_hash = hashlib.sha256(log_entry.encode("utf-8")).hexdigest()
        with open(log_file + ".hash", "a") as f:
            f.write(log_hash + "\n")
            


    # Function to configure colors
    def configure_colors():
        colors = {
            "color1": "#5a17d6",
            "color2": "#a37cf0",
            "color3": "#420889",
            "color4": "#8816ce",
            "color5": "#9980d1",
        }
        return colors

    # Function to send email notifications
    def send_email_notification(device, email_config):
        msg = EmailMessage()
        msg.set_content(
            f"Device: {device['name']}\nIP Address: {device['ip']}\nStatus: Unusual behaviour detected")

        msg["Subject"] = f"IoTShield Notification: {device['name']} ({device['ip']})"
        msg["From"] = email_config["from_email"]
        msg["To"] = email_config["to_email"]

        server = smtplib.SMTP_SSL(
            email_config["smtp_server"], email_config["smtp_port"])
        server.login(email_config["from_email"],
                    email_config["email_password"])
        server.send_message(msg)
        server.quit()

    # Function to generate PDF reports
    def generate_pdf_report(devices, byte_rates, anomalies, pdf_filename):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, "IoTShield Network Devices Report", ln=True, align="C")

        pdf.set_font("Arial", size=10)
        for idx, device in enumerate(devices):
            pdf.cell(
                0, 10, f"{idx + 1}. {device['name']} ({device['ip']})", ln=True)
            pdf.cell(
                0, 10, f"   In: {byte_rates[device['ip']]['in']} bytes, Out: {byte_rates[device['ip']]['out']} bytes", ln=True)
            if idx in anomalies:
                pdf.cell(0, 10, f"   Status: Anomaly Detected", ln=True)

        pdf.output(pdf_filename)

    # Function to securely log activities
    def log_activity(activity, log_filename):
        log_entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {activity}\n"
        log_entry_hash = hashlib.sha256(log_entry.encode("utf-8")).hexdigest()
        with open(log_filename, "a") as log_file:
            log_file.write(f"{log_entry}{log_entry_hash}\n")

    # Function to update GUI
    def update_gui(window, tree, devices, byte_rates, anomalies, email_config, log_filename):
        tree.delete(*tree.get_children())
        for idx, device in enumerate(devices):
            device_type = detect_device_type(device["name"])
            device_icon = get_device_icon(device_type)
            image = Image.open(device_icon).resize((24, 24))
            photo = ImageTk.PhotoImage(image)

            window.icon_cache[device["ip"]] = photo

            anomaly_status = "Anomaly" if idx in anomalies else "Normal"
            tree.insert("", "end", text=device["name"], image=photo, values=(
                device["ip"], byte_rates[device["ip"]]["in"], byte_rates[device["ip"]]["out"], anomaly_status))

            if anomaly_status == "Anomaly":
                send_email_notification(device, email_config)
                log_activity(
                    f"Anomaly detected for {device['name']} ({device['ip']})", log_filename)

        window.after(1000, update_gui, window, tree, devices,
                    byte_rates, anomalies, email_config, log_filename)                  

