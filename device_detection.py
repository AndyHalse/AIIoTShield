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
import paramiko

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

        self.subnet_mask = None
        self.default_gateway = None
        self.dhcp_server = None
        self.nic = None
        self.network_topology = None
        self.routing_protocol = None
        self.switches = []
        self.routers = []
        self.firewall = None
        self.ports = []
        self.vlans = []
        self.qos = None
        self.nat = None
        self.vpn = None
        self.remote_access_protocol = None
        self.authentication_and_authorization_mechanisms = []
        self.network_monitoring_and_management_tools = []
        self.bandwidth_utilization = None
        self.packet_loss = None
        self.latency = None
        self.network_security_protocols = []
        self.dns_resolution = None
        self.tcp_ip = None
        self.udp = None
        self.icmp = None
        self.ipsec = None
        self.ssl_tls_encryption = None
        self.snmp = None
        self.ntp = None
        self.dhcp_options = None
        self.devices = []

def scan_network(self, destination):
    # retrieve IP address of current host
    current_host = socket.gethostname()
    host_ip = socket.gethostbyname(current_host)

    # extract network address and netmask
    network_address = str(ipaddress.ip_network(
        host_ip + '/24', False).network_address)
    netmask = str(ipaddress.ip_network(
        host_ip + '/24', False).prefixlen)

    # reset devices list before scanning network
    self.devices = []

    # retrieve subnet mask and default gateway
    route_info = subprocess.check_output(
        "netstat -nr | grep '^default'".split()).decode().strip()
    subnet_mask = ''
    default_gateway = ''
    for line in route_info.split('\n'):
        if 'netmask' in line:
            subnet_mask = line.split()[-2]
        elif 'default' in line:
            default_gateway = line.split()[-2]

    self.subnet_mask = subnet_mask
    self.default_gateway = default_gateway

    # retrieve DNS servers and DHCP server
    dns_servers = netifaces.gateways()['default'][2]
    dhcp_server = subprocess.check_output(
        "networksetup -getinfo Ethernet | grep 'Server Identifier'".split()).decode().strip()
    dhcp_server = dhcp_server.split(': ')[-1]

    self.dns_servers = dns_servers
    self.dhcp_server = dhcp_server

    # get NIC information
    nic_info_lines = subprocess.check_output(
        "networksetup -listallhardwareports".split()).decode().strip().split('\n')
    nic_info = []
    for line in nic_info_lines[1:]:
        if 'Hardware Port' in line:
            # move initialization of nic_dict here
            nic_dict = {'Hardware Port': line.split(':')[1].strip()}
            for next_line in nic_info_lines[nic_info_lines.index(line)+1:]:
                if 'Ethernet Address' in next_line:
                    # create a new dictionary for each network interface
                    nic_dict['Ethernet Address'] = next_line.split(':')[-1].strip()
                    # append the dictionary to the list
                    nic_info.append(nic_dict)
                    break

    self.nic = nic_info

    # use nmap to scan for open ports
    nm = nmap.PortScanner()
    arguments = f"-sS -sV -O {network_address}/{netmask}"
    scan_results = nm.scan(arguments=arguments)
    for ip, results in scan_results['scan'].items():
        if results['status']['state'] == 'up':
            open_ports = []
            for port, data in results['tcp'].items():
                if data['state'] == 'open':
                    open_ports.append(port)

            # check the network topology
            topology_output = os.popen(f"traceroute {destination}").read()
            hops = []
            for line in topology_output.split('\n'):
                if 'traceroute to' in line:
                    continue
                if '  1 ' in line:
                    hops.append(line.split()[1])
                elif '\t2 ' in line:
                    hops.append(line.split()[1])
                elif '\t3 ' in line:
                    hops.append(line.split()[1])

            device = NetworkDevice(
                ip, results['addresses']['mac'], results.get('vendor', ''),
                subnet_mask, default_gateway, dns_servers, open_ports,
                dhcp_server, nic_info[0]['Hardware Port'],
                nic_info[0]['Ethernet Address'], netmask, hops)
            self.devices.append(device)
    return self.devices

           