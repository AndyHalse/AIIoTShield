import tkinter as tk
import tkinter.ttk as ttk
from tkintertable import TableCanvas, TableModel
from color_swatch import color_swatch
from device_detection import DeviceDetector

class Ui_IoTShield:
    def __init__(self, main_window):
        self.main_window = main_window
        self.create_widgets()
        self.main_frame = tk.Frame(self.main_window)

    def show_loading_popup(self):
        if self.loading_popup is not None:
            # The popup is already displayed
            return

        # Create a Toplevel widget for the popup
        self.loading_popup = tk.Toplevel(self.main_window)
        self.loading_popup.title("Scanning devices...")
        self.loading_popup.geometry("400x200")

        # Create a Label to display the loading message
        message_label = tk.Label(self.loading_popup, text="Scanning all devices on the network which may take time...")
        message_label.pack(pady=10)

        # Center the popup on the main window
        self.loading_popup.transient(self.main_window)
        x = self.main_window.winfo_rootx() + self.main_window.winfo_width() // 2 - self.loading_popup.winfo_width() // 2
        y = self.main_window.winfo_rooty() + self.main_window.winfo_height() // 2 - self.loading_popup.winfo_height() // 2
        self.loading_popup.geometry("+{}+{}".format(x, y))

        # Update the window to ensure the Label is displayed
        self.loading_popup.update_idletasks()

    def hide_loading_popup(self):
        if self.loading_popup is None:
            # The popup is not displayed
            return

        # Destroy the popup
        self.loading_popup.destroy()
        self.loading_popup = None

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
        self.create_device_table([])

    def create_buttons(self):
    # Create the buttons here
        button_bar = tk.Frame(self.main_frame)
        button_bar.pack(side="bottom", fill="x", pady=10)

        ttk.Button(button_bar, text="Scan Network", command=self.main_window.scan_devices, style="Cust.TButton").pack(side="left", padx=5)
        ttk.Button(button_bar, text="Logs", command=self.on_logs_button_clicked, style="Cust.TButton").pack(side="left", padx=5)
        ttk.Button(button_bar, text="Save to PDF", command=self.on_save_to_pdf_button_clicked, style="Cust.TButton").pack(side="left", padx=5)
        ttk.Button(button_bar, text="Help", command=self.on_help_button_clicked, style="Cust.TButton").pack(side="left", padx=5)
        ttk.Button(button_bar, text="Exit", command=self.main_window.on_close, style="Cust.TButton").pack(side="right", padx=5)

        self.style = ttk.Style()
        self.style.configure("Cust.TButton", foreground=color_swatch["primary"], background=color_swatch["secondary"], font=("Arial", 12, "bold"), width=20, height=2)

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

