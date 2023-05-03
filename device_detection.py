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
        self.csv_file = os.path.join(
            os.path.dirname(__file__), 'detected_devices.csv')

    # Check OS and chipset compatibility
    def check_compatibility(self):
        os_name = platform.system()
        if os_name != "Darwin":
            return False

        processor = platform.processor()
        if "Apple" not in processor:
            return False

        return True

    # Function to ping IP addresses
    def ping_ip(self, ip):
        param = "-n" if platform.system().lower() == "windows" else "-c"
        command = ["ping", param, "1", ip]
        return subprocess.call(command) == 0

    # Function to run nmap for device discovery
    def run_nmap(self, ip_range):
        nmap_cmd = f"nmap -sn {ip_range}"
        nmap_output = subprocess.check_output(
            nmap_cmd, shell=True).decode("utf-8")
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

    # Function to detect device type
    def detect_device_type(self, device_name):
        if "cctv" in device_name.lower():
            return "cctv"
        elif "echo" in device_name.lower():
            return "echo"
        elif "apple" in device_name.lower():
            return "apple_iot"
        else:
            return "unknown"

    # Function to calculate byte rates
    def calculate_byte_rates(self, devices):
        byte_rates = {}
        for device in devices:
            byte_rates[device["ip"]] = {"in": random.randint(
                1000, 10000), "out": random.randint(1000, 10000)}
        return byte_rates


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
