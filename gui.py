import tkinter as tk
import tkinter.ttk as ttk
from tkintertable import TableCanvas, TableModel
from color_swatch import color_swatch

class Ui_IoTShield:
    def __init__(self, main_window, parent=None):
        self.main_window = main_window
        self.create_widgets()

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
            data[index] = {"IP": device["ip"], "Hostname": device["hostname"], "MAC Address": device["mac"], "Device Type": device["device_type"], "Last Seen": device["last_seen"]}

        model = TableModel()
        model.importDict(data)

        self.table.setModel(model)
        self.table.redrawTable()

    def create_widgets(self):
        self.main_frame = tk.Frame(self.main_window)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.create_buttons()
        self.create_device_table([])

    def create_buttons(self):
    # Create the buttons here
        button_bar = tk.Frame(self.main_frame)
        button_bar.pack(side="bottom", fill="x", pady=10)

        ttk.Button(button_bar, text="Scan Devices", command=self.scan_devices, style="Cust.TButton").pack(side="left", padx=5)
        ttk.Button(button_bar, text="Logs", command=self.on_logs_button_clicked, style="Cust.TButton").pack(side="left", padx=5)
        ttk.Button(button_bar, text="Save to PDF", command=self.on_save_to_pdf_button_clicked, style="Cust.TButton").pack(side="left", padx=5)
        ttk.Button(button_bar, text="Help", command=self.on_help_button_clicked, style="Cust.TButton").pack(side="left", padx=5)
        ttk.Button(button_bar, text="Exit", command=self.main_window.on_close, style="Cust.TButton").pack(side=tk.RIGHT, padx=5)

        self.style = ttk.Style()
        self.style.configure("Cust.TButton", foreground=color_swatch["primary"], background=color_swatch["secondary"], font=("Arial", 12, "bold"), width=20, height=2)


    def scan_devices(self):
        self.main_window.scan_devices()

        print("Scanning devices...")

    def on_logs_button_clicked(self):
        # Implement the functionality you want when the Logs button is clicked
        print("Logs button clicked")  

    def on_help_button_clicked(self):
        # Implement the functionality you want when the Help button is clicked
        print("Help button clicked")

    def setup_ui(self):
        # Define the UI elements here
        self.create_buttons()

    def on_save_to_pdf_button_clicked(self):
        # Add the code to save the data to a PDF file here
        print("Saving to PDF...")

