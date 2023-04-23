import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox


class Ui_IoTShield(tk.Frame):
    def __init__(self, main_window, reload_data_func=None):
        super().__init__(main_window.main_frame)
        self.main_window = main_window
        self.reload_data_func = reload_data_func
        ...

    def update_device_table(self, devices):
        """
        Update the table with the list of detected devices.
        :param devices: The list of detected devices.
        """
        self.message_label.config(text=f"Detected {len(devices)} devices")
        self.tableWidget.delete(*self.tableWidget.get_children())
        for row, device in enumerate(devices):
            self.tableWidget.insert(parent='', index='end', values=(
                device["ip"],
                device["hostname"],
                device["device_type"],
                device["mac"],
                device["os"],
                device["cpu"],
                device["memory"],
                device["last_seen"]
            ))
