import tkinter as tk
from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
import tkinter

from gui_components import Ui_IoTShield
from abuse_detection import AbuseDetector

import logging


class AIIoTShield(tkinter.Toplevel):
    def __init__(self, main_window):
        self.setupUi(main_window)
        
        # Create instances of the Detector and DeviceDetector classes
        self.detector = Detector()
        self.device_detector = DeviceDetector(network_prefixes=[{"prefix": "192.168.0", "start": 1, "end": 255}],
                                               timeout=1)

        # Set up the UI
        self.ui = Ui_IoTShield()
        self.ui.setupUi(self)

        # Connect signals and slots
        self.ui.reload_data_button.clicked.connect(self.scan_devices)

    def scan_devices(self):
        # Start a thread to scan the network for devices
        self.ui.message_label.setText("Scanning for devices...")
        self.ui.progressBar.setValue(0)
        self.ui.reload_data_button.setEnabled(False)

        # Start a thread to scan the network for devices
        thread = NetworkScanThread(self.device_detector.network_prefixes, self.device_detector)
        thread.progress_update.connect(self.ui.progressBar.setValue)
        thread.devices_detected_signal.connect(self.update_device_table)
        thread.finished.connect(self.scan_complete)
        thread.start()

    def update_device_table(self, devices):
        # Update the table with the list of detected devices
        self.ui.message_label.setText(f"Detected {len(devices)} devices")
        self.ui.tableWidget.setRowCount(len(devices))
        for row, device in enumerate(devices):
            self.ui.tableWidget.setItem(row, 0, tkinter.ttk.Treeview(device["ip"]))
            self.ui.tableWidget.setItem(row, 1, tkinter.ttk.Treeview(device["mac"]))
            self.ui.tableWidget.setItem(row, 2, tkinter.ttk.Treeview(device["vendor"]))

    def scan_complete(self):
        # Enable the reload data button when the scan is complete
        self.ui.reload_data_button.setEnabled(True)


class GUIApp:
    def __init__(self):
        self.detector = Detector()
