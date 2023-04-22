import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter import messagebox


class Ui_IoTShield(tk.Frame):
    def __init__(self, main_window, reload_data_func=None):
        super().__init__(main_window.main_frame)
        self.main_window = main_window
        self.reload_data_func = reload_data_func
        ...


    # Remove the 'self' argument from the method signature
    def create_frame(title, parent):
        # Existing code

            # Create the UI elements here
            pass

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

    def create_ui(self):
        # Add UI elements to the frame
        self.message_label = ttk.Label(self, text="")
        self.message_label.pack(side="top", pady=5)

        self.progressBar = ttk.Progressbar(
            self, orient="horizontal", length=200, mode="determinate")
        self.progressBar.pack(side="top", pady=5)

        self.tableWidget = ttk.Treeview(self)
        self.setup_table_widget(self.tableWidget)
        self.tableWidget.pack(side="top", fill="both", expand=True)

        def setup_table_widget(self, table_widget):

            table_widget.setColumnCount(9)
            table_widget.setHorizontalHeaderLabels(
                ["Icon", "IP", "Name", "Type", "Version", "MAC", "CPU", "Memory", "Update"])
            header = table_widget.horizontalHeader()
            header.setSectionResizeMode(
                QHeaderView.ResizeMode.ResizeToContents)
            table_widget.horizontalHeader().setStretchLastSection(True)

    def search_devices(self, search_text):
        """
        Search the table for devices matching the given search text.
        :param search_text: The search text.
        """
        for i in range(self.tableWidget.rowCount()):
            match = False
            for j in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(i, j)
                if item and search_text.lower() in item.text().lower():
                    match = True
                    break
            self.tableWidget.setRowHidden(i, not match)

    def scan_devices(self):
        """
        Scan the network for devices and update the table with the results.
        """
        # Start a thread to scan the network for devices
        self.message_label.setText("Scanning for devices...")
        self.progressBar.setValue(0)
        self._button.setEnabled(False)

        thread = NetworkScanThread(
            self.device_detector.network_prefixes, self.device_detector)
        thread.progress_update.connect(self.progressBar.setValue)
        thread.devices_detected_event.connect(self.update_device_table)
        thread.finished.connect(self.scan_complete)
        thread.start()

    def update_device_table(self, devices):
        """
        Update the table with the list of detected devices.
        :param devices: The list of detected devices.
        """
        self.message_label.setText(f"Detected {len(devices)} devices")
        self.tableWidget.setRowCount(len(devices))
        for row, device in enumerate(devices):
            item = QTableWidgetItem(device["ip"])
            self.tableWidget.setItem(row, 0, item)
            item = QTableWidgetItem(device["hostname"])
            self.tableWidget.setItem(row, 1, item)
            item = QTableWidgetItem(device["device_type"])
            self.tableWidget.setItem(row, 2, item)
            item = QTableWidgetItem(device["mac"])
            self.tableWidget.setItem(row, 3, item)
            item = QTableWidgetItem(device["os"])
            self.tableWidget.setItem(row, 4, item)
            item = QTableWidgetItem(device["cpu"])
            self.tableWidget.setItem(row, 5, item)
            item = QTableWidgetItem(device["memory"])
            self.tableWidget.setItem(row, 6, item)
            item = QTableWidgetItem(device["last_seen"])
            self.tableWidget.setItem(row, 7, item)

    def scan_complete(self):
        """
        Called when the network scan is complete.
        """
        self._button.setEnabled(True)

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
