import logging
import tkinter
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter import messagebox
from clustering import DeviceClustering

from abuse_detection import AbuseDetector


class AIIoTShield(tkinter.Toplevel):
    def __init__(self, main_window):
        self.setupUi(main_window)
        
        # Create instances of the Detector and DeviceDetector classes
        self.detector = Detector()
        # Set up the UI
        self.ui = Ui_IoTShield()
        self.ui.setupUi(self)

        # Connect signals and slots
        self.ui.reload_data_button.clicked.connect(self.scan_devices)
        self.update_device_list(devices)

    def scan_devices(self):
        from device_detection import DeviceDetector
        self.device_detector = DeviceDetector()
        devices = self.device_detector.scan_devices()
        device_clustering = DeviceClustering(devices)
        clustered_devices = device_clustering.cluster_devices()

        self.update_device_list(clustered_devices)

        # Start a thread to scan the network for devices
        thread = NetworkScanThread(self.device_detector.self.device_detector)
        thread.progress_update.connect(self.ui.progressBar.setValue)
        thread.devices_detected_signal.connect(self.update_device_table)
        thread.finished.connect(self.scan_complete)
        thread.start()

    def scan_complete(self):
        # Enable the reload data button when the scan is complete
        self.ui.reload_data_button.setEnabled(True)


class GUIApp:
    def __init__(self):
        self.detector = Detector()
