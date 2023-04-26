import os
import sys
import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk

from device_detector import DeviceDetector
from PIL import Image, ImageTk
from tkintertable import TableCanvas, TableModel

from color_swatch import color_swatch
from device_clustering import DeviceClustering

dir_path = os.path.dirname(os.path.realpath(__file__))


class Ui_IoTShield:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Cyber IoT Shield")
        self.loading_popup = None
        self.device_detector = device_detector
        self.device_detector.place(x=10, y=10, width=820, height=100)
        self.ui.place(x=10, y=120, width=820, height=650)

        self.scan_button = ttk.Button(self.root, text="Scan devices", command=self.device_detector.scan_devices)
        self.scan_button.grid(row=1, column=0, padx=10, pady=10)

        self.root.title("AI IoT Shield")
        self.root.geometry("840x780")

        self.root.config(bg="white")
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.create_buttons()
        self.create_listbox()
        self.create_labels()
        self.create_entry_fields()
        self.create_widgets()

        self.frame_1 = tk.Frame(self.root, bg="white")
        self.frame_1.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.frame_2 = tk.Frame(self.root, bg="white")
        self.frame_2.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.frame_3 = tk.Frame(self.root, bg="white")
        self.frame_3.pack(side="bottom", fill="both", expand=True, padx=10, pady=10)

    def setupUi(self):
            # ... other UI setup code ...
            self.reload_data_button = tk.Button(self.parent, text="Reload Data", command=self.parent.scan_devices)
            self.reload_data_button.pack()

    def show_loading_popup(self):
        if self.loading_popup is not None:
            return

        # Create a Toplevel widget for the popup
        self.loading_popup = tk.Toplevel(self.parent)
        self.loading_popup.title("Scanning devices...")
        self.loading_popup.geometry("800x400")

        # Create a Label to display the loading message
        message_label = tk.Label(self.loading_popup, text="Scanning all devices on the network which may take time...")
        message_label.pack(pady=10)

        # Center the popup on the parent window
        self.loading_popup.transient(self.parent)
        x = self.parent.winfo_rootx() + self.parent.winfo_width() // 2 - self.loading_popup.winfo_width() // 2
        y = self.parent.winfo_rooty() + self.parent.winfo_height() // 2 - self.loading_popup.winfo_height() // 2
        self.loading_popup.geometry("+{}+{}".format(x, y))

        # Create a progress bar widget
        progress = ttk.Progressbar(self.loading_popup, orient=tk.HORIZONTAL, length=300, mode='indeterminate')
        progress.pack(pady=10)

        # Start the progress bar animation
        progress.start()
        self.loading_popup.update_idletasks()

    def hide_loading_popup(self):
        if self.loading_popup is None:
            return

        # Destroy the popup
        self.loading_popup.destroy()
        self.loading_popup = None

    def create_buttons(self):
        button_bar = tk.Frame(self.root, bg="#e0e0e0")
        button_bar.pack(fill="x", pady=5, padx=5)

        ttk.Button(button_bar, text="Scan Network", command=self.device_detector.scan_devices, style="Cust.TButton").pack(side="left", padx=5)
        ttk.Button(button_bar, text="Exit", command=self.device_detector.on_close, style="Cust.TButton").pack(side="right", padx=5)

        ttk.Button(button_bar, text="Logs", command=self.device_detector.on_logs_button_clicked, style="Cust.TButton").pack(side="left",
                                                                                                            padx=5)
        ttk.Button(button_bar, text="Save to PDF", command=self.device_detector.on_save_to_pdf_button_clicked,
                   style="Cust.TButton").pack(side="left", padx=5)
        ttk.Button(button_bar, text="Help", command=self.device_detector.on_help_button_clicked, style="Cust.TButton").pack(side="left",
                                                                                                            padx=5)

        self.style = ttk.Style()
        self.style.configure("Cust.TButton", foreground=color_swatch["primary"], background=color_swatch["secondary"],
                             font=("Arial", 12, "bold"), width=20, height=2)

    def on_logs_button_clicked(self):
        # Implement the functionality you want when the Logs button is clicked
        # Show a sample logs message as a pop-up. Replace this with your actual logs.
        showinfo(title="Logs", message="Sample logs message...")

    def on_help_button_clicked(self):
        # Implement the functionality you want when the Help button is clicked
        # Show a sample help message as a pop-up. Replace this with your actual help content.
        showinfo(title="Help", message="Help message: \n1. Scan Network: Scans the network for devices.\n2. Save to PDF: Save the device list to a PDF file.")

    def on_save_to_pdf_button_clicked(self):
        # Add the code to save the data to a PDF file here
        print("Saving to PDF...")

        # Sample data to be saved as PDF. Replace this with the actual device list from the table.
        devices = [
            {"IP": "192.168.0.1", "Hostname": "router", "MAC Address": "00:11:22:33:44:55", "Device Type": "Router", "Last Seen": "2023-04-25 10:00:00"},
            {"IP": "192.168.0.2", "Hostname": "laptop", "MAC Address": "00:11:22:33:44:56", "Device Type": "Laptop", "Last Seen": "2023-04-25 10:05:00"}
        ]

        pdf_file = "device_list.pdf"
        pdf_document = canvas.Canvas(pdf_file, pagesize=letter)
        pdf_document.setTitle("Device List")

        pdf_document.setFont("Helvetica-Bold", 16)
        pdf_document.drawString(50, 750, "Device List")

        pdf_document.setFont("Helvetica", 12)
        header = ["IP", "Hostname", "MAC Address", "Device Type", "Last Seen"]
        y_position = 700
        x_position = 50

        for index, field in enumerate(header):
            pdf_document.drawString(x_position + index * 120, y_position, field)

        y_position -= 20

        for device in devices:
            for index, field in enumerate(header):
                pdf_document.drawString(x_position + index * 120, y_position, str(device[field]))
            y_position -= 20

        pdf_document.save()
        print(f"Saved device list to {pdf_file}")


    def update_device_list(self, clusters):
        self.device_list.delete(0, tk.END)
        for i, cluster in enumerate(clusters):
            self.device_list.insert(tk.END, f"Cluster {i + 1}:")
            for device in cluster:
                self.device_list.insert(tk.END, f"  - {device['ip']} ({device['hostname']})")

    def _resize_handler(self, event):
        if self._ui_ready:
            self.left_frame.config(width=int(event.width/3))
            self.right_frame.config(width=int(event.width/3*2))

    


    def create_device_table(self, devices):
        self.table_frame = tk.Frame(self.main_frame)
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.table = TableCanvas(self.table_frame, editable=False)
        self.table.show()

        self.update_device_table(devices)

    def update_device_table(self, devices):
        header = ["IP", "Hostname", "MAC Address", "Device Type", "Last Seen"]
        data = {}
        for index, device in enumerate(devices):
            data[index] = {"IP": device["ip"], "Hostname": device["hostname"], "MAC Address": device["mac"],
                           "Device Type": device["device_type"], "Last Seen": device["last_seen"]}

        model = TableModel()
        model.importDict(data)

        self.table.setModel(model)
        self.table.redrawTable()

    def on_logs_button_clicked(self):
        # Implement the functionality you want when the Logs button is clicked
        # Show a sample logs message as a pop-up. Replace this with your actual logs.
        showinfo(title="Logs", message="Sample logs message...")

    def on_help_button_clicked(self):
        # Implement the functionality you want when the Help button is clicked
        # Show a sample help message as a pop-up. Replace this with your actual help content.
        showinfo(title="Help", message="Help message: \n1. Scan Network: Scans the network for devices.\n2. Save to PDF: Save the device list to a PDF file.")

    def on_save_to_pdf_button_clicked(self):
        # Add the code to save the data to a PDF file here
        print("Saving to PDF...")

        # Sample data to be saved as PDF. Replace this with the actual device list from the table.
        devices = [
            {"IP": "192.168.0.1", "Hostname": "router", "MAC Address": "00:11:22:33:44:55", "Device Type": "Router", "Last Seen": "2023-04-25 10:00:00"},
            {"IP": "192.168.0.2", "Hostname": "laptop", "MAC Address": "00:11:22:33:44:56", "Device Type": "Laptop", "Last Seen": "2023-04-25 10:05:00"}
        ]

        pdf_file = "device_list.pdf"
        pdf_document = canvas.Canvas(pdf_file, pagesize=letter)
        pdf_document.setTitle("Device List")

        pdf_document.setFont("Helvetica-Bold", 16)
        pdf_document.drawString(50, 750, "Device List")

        pdf_document.setFont("Helvetica", 12)
        header = ["IP", "Hostname", "MAC Address", "Device Type", "Last Seen"]
        y_position = 700
        x_position = 50

        for index, field in enumerate(header):
            pdf_document.drawString(x_position + index * 120, y_position, field)

        y_position -= 20

        for device in devices:
            for index, field in enumerate(header):
                pdf_document.drawString(x_position + index * 120, y_position, str(device[field]))
            y_position -= 20

        pdf_document.save()
        print(f"Saved device list to {pdf_file}")

