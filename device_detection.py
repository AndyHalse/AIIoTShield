import csv
import hashlib
import ipaddress
import os
import socket
import subprocess
from datetime import datetime

import netifaces
import nmap
from nmap import PortScanner
from PIL import Image, ImageTk
from sklearn.cluster import KMeans


class NetworkDevice:
    def __init__(self, ip_address, mac_address, vendor_name, device_type, os, os_version, open_ports, subnet_info, dhcp_info, network_info, security_info):
        self.ip_address = ip_address
        self.mac_address = mac_address
        self.vendor_name = vendor_name
        self.device_type = device_type
        self.os = os
        self.os_version = os_version
        self.open_ports = open_ports 
        self.subnet_info = subnet_info
        self.dhcp_info = dhcp_info
        self.network_info = network_info
        self.security_info = security_info

        self.subnet_mask = subnet_mask
        self.default_gateway = default_gateway
        self.dhcp_server = dhcp_server
        self.nic = nic
        self.network_topology = network_topology
        self.routing_protocol = routing_protocol
        self.switches = switches
        self.routers = routers
        self.firewall = firewall
        self.ports = ports
        self.vlans = vlans
        self.qos = qos
        self.nat = nat
        self.vpn = vpn
        self.remote_access_protocol = remote_access_protocol
        self.authentication_and_authorization_mechanisms = authentication_and_authorization_mechanisms
        self.network_monitoring_and_management_tools = network_monitoring_and_management_tools
        self.bandwidth_utilization = bandwidth_utilization
        self.packet_loss = packet_loss
        self.latency = latency
        self.network_security_protocols = network_security_protocols
        self.dns_resolution = dns_resolution
        self.tcp_ip = tcp_ip
        self.udp = udp
        self.icmp = icmp
        self.ipsec = ipsec
        self.ssl_tls_encryption = ssl_tls_encryption
        self.snmp = snmp
        self.ntp = ntp
        self.dhcp_options = dhcp_options
        self.devices = []

    def scan_network(self):
        # retrieve IP address of current host
        current_host = socket.gethostname()
        host_ip = socket.gethostbyname(current_host)

        # extract network address and netmask
        network_address = str(ipaddress.ip_network(host_ip + '/24', False).network_address)
        netmask = str(ipaddress.ip_network(host_ip + '/24', False).prefixlen)

        # reset devices list before scanning network
        self.devices = []

        # retrieve subnet mask and default gateway
        route_info = subprocess.check_output("route -n get default".split()).decode().strip()
        subnet_mask = ''
        default_gateway = ''
        for line in route_info.split('\n'):
            if 'netmask' in line:
                subnet_mask = line.split()[-1]
            elif 'gateway' in line:
                default_gateway = line.split()[-1]

        # retrieve DNS servers and DHCP server
        dns_servers = netifaces.gateways()['default'][2]
        dhcp_server = subprocess.check_output("ipconfig getoption en0 server_identifier".split()).decode().strip()

        # get NIC information
        nic = subprocess.check_output("networksetup -listallhardwareports".split()).decode().strip()

        # get network topology
        network_topology = subprocess.check

    @staticmethod
    def clean_ua(user_agent):
        try:
            # code to clean user agent
            pass
        except Exception as e:
            print(f"Error cleaning user agent: {e}")
            return ''

    def __str__(self):
        return f'{self.ip_address} {self.mac_address} ({self.vendor_name})'


    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.mac_address == other.mac_address

    def __hash__(self):
        return hash(self.mac_address)

    def to_dict(self):
        return {
            'ip_address': self.ip_address,
            'mac_address': self.mac_address,
            'vendor_name': self.vendor_name,
            'device_type': self.device_type,
            'os': self.os,
            'os_version': self.os_version,
            'open_ports': self.open_ports,
            'dns': self.dns
        }

    def __str__(self):
        return f'{self.ip_address} {self.mac_address} ({self.vendor_name})'


    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.mac_address == other.mac_address

    def __hash__(self):
        return hash(self.mac_address)

    def to_dict(self):
        return {
            'ip_address': self.ip_address,
            'mac_address': self.mac_address,
            'vendor_name': self.vendor_name,
            'device_type': self.device_type,
            'os': self.os,
            'os_version': self.os_version,
            'open_ports': self.open_ports,
            'dns': self.dns
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['ip_address'], data['mac_address'], data['vendor_name'],
            data['device_type'], data['os'], data['os_version'], data['open_ports'], data['dns']
        )


    def cluster_devices(self):
        ips = [ipaddress.ip_address(device.ip_address) for device in self.devices]
        kmeans = KMeans(n_clusters=min(5, len(ips)), random_state=0).fit([[int(ip)] for ip in ips])
        cluster_labels = kmeans.labels_

        for i, device in enumerate(self.devices):
            device.model = f"Cluster {cluster_labels[i]+1}"

    def get_detected_devices(self):
        return self.devices

    def save_devices_csv(self):
        with open(self.csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["IP Address", "Hostname"])
            writer.writerows(self.devices)

    # Function to generate secure logs
    def generate_secure_log(self, log_entry):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - {log_entry}\n"

        with open(self.csv_file, "a") as f:
            f.write(log_entry)

        log_hash = hashlib.sha256(log_entry.encode("utf-8")).hexdigest()
        with open(self.csv_file + ".hash", "a") as f:
            f.write(log_hash + "\n")

    # Function to securely log activities
    def log_activity(self, activity):
        log_entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {activity}\n"
        log_entry_hash = hashlib.sha256(log_entry.encode("utf-8")).hexdigest()
        with open(self.csv_file, "a") as log_file:
            log_file.write(f"{log_entry}{log_entry_hash}\n")
