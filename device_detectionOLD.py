import csv
import datetime
import hashlib
import os
import socket
import subprocess
import tkinter as tk
import ipaddress
from nmap import PortScanner
from PIL import Image, ImageTk
from sklearn.cluster import KMeans

class DetectedDevice:
    def __init__(self, ip_address, mac_address, vendor_name, model, cpu_data, memory_data, device_type, dns):
        self.ip_address = ip_address
        self.mac_address = mac_address
        self.vendor_name = vendor_name
        self.model = model
        self.cpu_data = cpu_data
        self.memory_data = memory_data
        self.device_type = device_type
        self.dns = dns

class DeviceDetector:
    def __init__(self, ip_range, device_list):
        self.ip_range = ip_range
        self.csv_file = os.path.join(os.path.dirname(__file__), 'detected_devices.csv')
        self.devices = []
        self.device_list = device_list
        self.network = ipaddress.ip_network(ip_range)
        self.nmap_scanner = PortScanner()

    def detect(self):
        # Reset devices list
        self.devices = []

        # Use nmap to detect devices on network
        self.nmap_scanner.scan(hosts=self.ip_range, arguments='-sn')
        all_hosts = self.nmap_scanner.all_hosts()

        # Iterate over hosts and choose the ones which are up
        for host in all_hosts:
            if self.nmap_scanner[host].state() == 'up':
                # The next two lines were causing errors if the mac address or vendor were not found
                # Fixed the issue by checking if they exist before trying to get them
                addresses = self.nmap_scanner[host]['addresses']
                mac_address = addresses['mac'] if 'mac' in addresses else None
                vendors = self.nmap_scanner[host]['vendor']
                vendor_name = vendors.get(mac_address, None) if vendors and mac_address else None

                model = self.identify_device_type(vendor_name, host, mac_address)
                cpu_data = self.get_cpu_data(host)
                memory_data = self.get_memory_data(host)
                device_type = self.get_device_type(host)
                dns = self.get_dns(host)

                device = DetectedDevice(ip_address=host,
                                        mac_address=mac_address,
                                        vendor_name=vendor_name,
                                        model=model,
                                        cpu_data=cpu_data,
                                        memory_data=memory_data,
                                        device_type=device_type,
                                        dns=dns)
                self.devices.append(device)

        return self.devices

    def get_ipv4_network(self):
        for interface in socket.if_nameindex():
            addrs = socket.ifaddresses(interface[0])
            for addr in addrs.get(socket.AF_INET, []):
                ip = ipaddress.ip_address(addr['addr'])
                if not ip.is_private:
                    # Obtain the network object directly from the IP interface
                    return ipaddress.ip_interface(str(ip) + '/' + str(addr['netmask'])).network
        # If no network is found, raise an exception
        raise ValueError("No public IPv4 network found in interfaces")


    def detect_devices(self):
        # Detect devices on the network
        nmap_scanner = PortScanner()
        nmap_scanner.scan(hosts=self.ip_range, arguments='-sn')
        hosts_list = [(x, nmap_scanner[x]['status']['state']) for x in nmap_scanner.all_hosts()]

        # Update the GUI with the detected devices
        self.device_list.delete(0, tk.END)
        for host, status in hosts_list:
            if status == 'up':
                self.device_list.insert(tk.END, host)

    def save_unknown_devices(self, unknown_devices):
        if len(unknown_devices) == 0:
            return
        with open(self.csv_file, 'a', newline='') as file:
            writer = csv.writer(file)
            for device in unknown_devices:
                writer.writerow([device.ip_address, device.mac_address, device.vendor_name, device.model, device.cpu_data, device.memory_data, device.device_type, device.dns])


    def run_nmap(self):
        nmap_cmd = f"nmap -sn {self.ip_range}"  # Add a closing quotation mark
        nmap_output = subprocess.check_output(nmap_cmd, shell=True).decode("utf-8")  # Execute the command
        return nmap_output

    def parse_nmap_output(self, nmap_output):
        devices = []
        
        # Check if the input argument is a string
        if not isinstance(nmap_output, str):
            raise TypeError("Input must be a string.")
            
        lines = nmap_output.split("\n")
        # Iterate over lines of nmap_output
        for i, line in enumerate(lines):
            # Check if the line contains "Nmap scan report for"
            if "Nmap scan report for" in line:
                device = {}
                # Split the line into words and use the last word as the IP address of the device
                device["ip"] = line.split()[-1]
                # Check if the next line contains "Host is up". If yes, set the "status" key of device to "up",
                # otherwise set it to "down"
                if i+1 < len(lines) and "Host is up" in lines[i+1]:
                    device["status"] = "up"
                else:
                    device["status"] = "down"
                # Check if the line after the next line contains "MAC Address:". If yes, split the line into words
                # and use the last word as the MAC address of the device, otherwise set "mac" key of the device to ""
                if i+2 < len(lines) and "MAC Address:" in lines[i+2]:
                    device["mac"] = lines[i+2].split()[-1]
                else:
                    device["mac"] = ""
                    
                devices.append(device)
        
        # Return the list of devices
        return devices

    def get_device_models(self):
        devices = self.device_detector.detect()
        return [device.model for device in devices]

    def scan_network(self):
        try:
            if self.device_detector is None:
                print("DeviceDetector is not available.")
                return

            devices = self.device_detector.detect()
            for device in devices:
                self.table.insert("", tk.END, values=[device.ip_address, device.mac_address, device.vendor_name, device.model])
            self.saved_data += devices
            self.device_combobox['values'] = self.get_device_models()
            self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        except Exception as e:
            print(f"Error scanning network: {e}")

    def get_device_icon(self, device_type):
        icons = {
            "cctv": "cctv_icon.png",
            "echo": "echo_icon.png",
            "apple_iot": "apple_iot_icon.png",
            "unknown": "unknown_icon.png",
        }
        return icons.get(device_type, "unknown_icon.png")


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
        device_type = None
        ssh = self.connect_to_device(ip_address, 'root', 'password')
        if ssh is not None:
            try:
                if vendor_name is not None:
                    if 'cisco' in vendor_name.lower():
                        device_type = 'cisco'
                    elif 'juniper' in vendor_name.lower():
                        device_type = 'juniper'
                    elif 'dell' in vendor_name.lower():
                        device_type = 'dell'
            except Exception as e:
                print(str(e))

            finally:
                ssh.close()

        return device_type

    # Function to generate secure logs
    def generate_secure_log(log_file, action):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - {action}\n"

        with open(log_file, "a") as f:
            f.write(log_entry)

        log_hash = hashlib.sha256(log_entry.encode("utf-8")).hexdigest()
        with open(log_file + ".hash", "a") as f:
            f.write(log_hash + "\n")

    # Function to securely log activities
    def log_activity(activity, log_filename):
        log_entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {activity}\n"
        log_entry_hash = hashlib.sha256(log_entry.encode("utf-8")).hexdigest()
        with open(log_filename, "a") as log_file:
            log_file.write(f"{log_entry}{log_entry_hash}\n")
