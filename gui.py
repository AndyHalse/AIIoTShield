import tkinter as tk
import tkinter.ttk as ttk

color_swatch = {
    "primary": "#5a17d6",
    "secondary": "#a37cf0",
    "tertiary": "#420889",
    "quaternary": "#8816ce",
    "quinary": "#9980d1"
}


class Ui_IoTShield(tk.Frame):
    def __init__(self, main_window, reload_data_func=None):
        super().__init__(main_window.main_frame)
        self.main_window = main_window
        self.reload_data_func = reload_data_func
        ...

    def create_widgets(self):
        # create UI widgets here
        # Create the UI elements here
        pass

    def create_buttons(self):
        # Create the buttons here
        button_bar = tk.Frame(self)
        button_bar.pack(side="bottom", fill="x", pady=10)

        ttk.Button(button_bar, text="Scan Devices", command=self.scan_devices,
                   style="Cust.TButton").pack(side="left", padx=5)
        ttk.Button(button_bar, text="Save to PDF", command=self.on_save_to_pdf_button_clicked,
                   style="Cust.TButton").pack(side="left", padx=5)
        ttk.Button(button_bar, text="Logs", command=self.on_logs_button_clicked,
                   style="Cust.TButton").pack(side="left", padx=5)
        ttk.Button(button_bar, text="Help", command=self.on_help_button_clicked,
                   style="Cust.TButton").pack(side="left", padx=5)

        # Exit button
        exit_button = ttk.Button(
            button_bar, text="Exit", command=self.main_window.on_close, style="Cust.TButton")
        exit_button.pack(side="left", padx=5, pady=5)

        button_bar.pack(side="top", fill="x", pady=10)

        self.style = ttk.Style()
        self.style.configure("Cust.TButton", foreground=color_swatch["primary"], background=color_swatch["secondary"], font=(
            "Arial", 12, "bold"), width=20, height=2)

    def update_device_table(self, devices):
        # Update the table with the list of detected devices
        self.ui.message_label.config(text=f"Detected {len(devices)} devices")
        self.ui.tableWidget.delete(*self.ui.tableWidget.get_children())
        for row, device in enumerate(devices):
            self.ui.tableWidget.insert("", "end", values=(
                device["ip"], device["mac"], device["vendor"]))

    def scan_complete(self):
        # Enable the reload data button when the scan is complete
        self.ui.reload_data_button.config(state="normal")

    def sort_column(self, tree, col, reverse):
        """Sorts the treeview columns when header is clicked"""
        l = [(tree.set(k, col), k) for k in tree.get_children('')]
        try:
            l.sort(key=lambda t: int(t[0]), reverse=reverse)
        except ValueError:
            l.sort(reverse=reverse)

        for index, (val, k) in enumerate(l):
            tree.move(k, '', index)

        tree.heading(col, command=lambda: self.sort_column(
            tree, col, not reverse))


class MainWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.ui = Ui_IoTShield(self)
        self.ui.pack(side="top", fill="both", expand=True)

        # Set network prefixes to empty list and timeout to 1 second
        self.network_prefixes = []
        self.timeout = 1

        # Create DeviceDetector object
        self.detector = DeviceDetector(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')

        # Set table headers
        for col in ("IP Address", "MAC Address", "Vendor"):
            self.ui.tableWidget.heading(col, text=col)

        # Call update_device_table with empty list to initialize table
        self.update_device_table([])

        # Set window title and size
        self.title("IoTShield")
        self.geometry("1024x768")

        # Connect scan_devices method to Scan Devices button
        self.ui.scan_devices_button.config(command=self.scan_devices)

        # Create QTimer object to update progress bar
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress_bar)
        # Change this value to adjust the progress bar speed
        self.timer.start(1000)

    def update_device_table(self, devices):
        # Update the table with the list of detected devices
        self.ui.message_label.config(text=f"Detected {len(devices)} devices")
        self.ui.tableWidget.delete(*self.ui.tableWidget.get_children())
        for device in devices:
            self.ui.tableWidget.insert("", "end", values=(
                device["ip"], device["mac"], device["vendor"]))

    def scan_complete(self):
        # Enable the scan devices button when the scan is complete
        self.ui.scan_devices_button.config(state="normal")

    def scan_devices(self):
        # Disable the scan devices button while scanning
        self.ui.scan_devices_button.config(state="disabled")

        devices = []
        for network_prefix in self.network_prefixes:
            prefix = network_prefix["prefix"]
            start = network_prefix["start"]
            end = network_prefix["end"]
            devices.extend(self.detector.parallel_scan(
                prefix, start, end, self.scan_complete))

        self.update_device_table(devices)

    def update_progress_bar(self):
        self.ui.progress_bar["value"] += 1
        if self.ui.progress_bar["value"] == self.ui.progress_bar["maximum"]:
            self.ui.progress_bar["value"] = 0

    def on_save_to_pdf_button_clicked(self):
        # Save table contents to PDF file
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            with open(file_path, "wb") as f:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                for i, col in enumerate(("IP Address", "MAC Address", "Vendor")):
                    pdf.cell(40, 10, col, 1)
                pdf.ln()
                for device in self.devices:
                    pdf.cell(40, 10, device["ip"], 1)
                    pdf.cell(40, 10, device["mac"], 1)
                    pdf.cell(40, 10, device["vendor"], 1)
                    pdf.ln()
                pdf.output(f)

    def update_progress_bar(self):
        self.ui.progress_bar.setValue(self.ui.progress_bar.value() + 1)

    def reload_data(self):
        self.ui.progress_bar.setValue(0)
        self.ui.header_label.setText("Reloading data...")

        devices = []
        for network_prefix in self.network_prefixes:
            prefix = network_prefix["prefix"]
            start = network_prefix["start"]
            end = network_prefix["end"]
            devices.extend(self.detector.parallel_scan(
                prefix, start, end, self.reload_data_func))

        self.devices = devices
        self.update_table(self.devices)
        self.ui.header_label.setText("Data reloaded")

    def on_logs_button_clicked(self):
        # Display the logs in a new window
        logs_window = tk.Toplevel(self)
        logs_window.title("Logs")

        logs_text = tk.Text(logs_window, width=100, height=50)
        logs_text.pack(fill="both", expand=True)

        with open("logs.txt", "r") as f:
            logs_text.insert("1.0", f.read())

    def on_help_button_clicked(self):
        # Open the user manual PDF file
        try:
            os.startfile("user_manual.pdf")
        except OSError:
            messagebox.showerror("Error", "Unable to open user manual")
