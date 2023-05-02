import tkinter as tk
from tkinter import ttk
from device_detector import DeviceDetector

class IoTShieldGUI:
    def __init__(self, title="IoT Shield", width=800, height=600):
        self.title = title
        self.width = width
        self.height = height
        self.saved_data = []
        self.device_detector = DeviceDetector("Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
        self.root = tk.Tk()
        self.root.title(self.title)
        self.root.geometry(f"{self.width}x{self.height}")

        self.menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Save", command=self.save_data)
        file_menu.add_command(label="Reload", command=self.reload_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Scan Network", command=self.scan_network)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)

        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="Help", command=self.show_help)
        help_menu.add_command(label="About", command=self.show_about)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=self.menu_bar)

        self.toolbar = tk.Frame(self.root)
        scan_button = ttk.Button(self.toolbar, text="Scan", command=self.scan_network)
        scan_button.pack(side=tk.LEFT, padx=2, pady=2)

        device_label = ttk.Label(self.toolbar, text="Devices:")
        device_label.pack(side=tk.LEFT, padx=2, pady=2)

        self.device_combobox = ttk.Combobox(self.toolbar, values=self.get_device_models())
        self.device_combobox.pack(side=tk.LEFT, padx=2, pady=2)

        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.table_frame = ttk.Frame(self.root)
        self.create_table()
        self.table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def create_table(self):
        columns = ("IP Address", "MAC Address", "Device Manufacturer", "Device Name")
        self.table = ttk.Treeview(self.table_frame, columns=columns, show="headings")

        for col in columns:
            self.table.heading(col, text=col)

        self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        devices = self.device_detector.detect_devices()
        device_types = [device.type for device in devices] # new list to store device types
        for device in devices:
            self.table.insert("", tk.END, values=[device.ip_address, device.mac_address, device.vendor_name, device.model])

        self.device_combobox['values'] = list(set(device_types)) # populate unique device types in combobox

    def get_device_models(self):
        devices = self.device_detector.detect_devices()  # modified here
        return [device.model for device in devices]

    def save_data(self):
        print("Save data")
        pass

    def scan_network(self):
        print("Scan network")

    def reload_data(self):
        print("Reload data")

    def show_help(self):
        print("Showing help")

    def show_about(self):
        print("Showing about")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = IoTShieldGUI()
    app.root.mainloop()
