import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

class Ui_IoTShield(tk.Frame):
    def __init__(self, main_window, reload_data_func=None):
        super().__init__(main_window.main_frame)
        self.main_window = main_window
        self.reload_data_func = reload_data_func
        ...

    def create_buttons(self):
        # Create the button bar
        button_bar = tk.Frame(self)

        # Save to PDF button
        save_to_pdf_button = ttk.Button(
            button_bar, text="Save to PDF", command=self.on_save_to_pdf_button_clicked)
        save_to_pdf_button.pack(side="left", padx=5, pady=5)

        # Logs button
        logs_button = ttk.Button(
            button_bar, text="Logs", command=self.on_logs_button_clicked)
        logs_button.pack(side="left", padx=5, pady=5)

        # Data Reload button
        reload_data_button = ttk.Button(
            button_bar, text="Data Reload", command=self.reload_data_button)
        reload_data_button.pack(side="left", padx=5, pady=5)

        # Help button
        help_button = ttk.Button(
            button_bar, text="Help", command=self.on_help_button_clicked)
        help_button.pack(side="left", padx=5, pady=5)

        # Exit button
        exit_button = ttk.Button(
            button_bar, text="Exit", command=self.main_window.on_close)
        exit_button.pack(side="left", padx=5, pady=5)

        button_bar.pack(side="top", fill="x")

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

    def on_save_to_pdf_button_clicked(self):
        """
        Called when the "Save to PDF" button is clicked.
        """
        # Implement functionality to save the table to a PDF file
        pass

    def on_logs_button_clicked(self):
        """
        Called when the "Logs" button is clicked.
        """
        # Implement functionality to show the log files
        pass

    def on_help_button_clicked(self):
        """
        Called when the "Help" button is clicked.
        """
        # Implement functionality to show the help page
        pass
