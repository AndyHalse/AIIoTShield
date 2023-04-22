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


