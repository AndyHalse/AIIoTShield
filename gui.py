import tkinter as tk
from tkinter import ttk, messagebox
import psutil
from device_detection import CustomDeviceDetector

class IoTShieldGUI:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("IoTShield")
        self.parent.geometry("1200x600")
        self.devices = []
        self.device_detector = CustomDeviceDetector(parent)

        main_frame = tk.Frame(parent)
        main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create the menu bar
        menu_bar = tk.Menu(self.parent)

        # Create the File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Save")
        file_menu.add_command(label="Exit", command=self.parent.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Create the Help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Help", command=self.show_help)
        help_menu.add_command(label="About")
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.parent.config(menu=menu_bar)

        # Create the toolbar
        toolbar = ttk.Frame(self.parent)

        # Set the style of the buttons
        style = ttk.Style()
        style.configure("TButton", background="red", foreground="white", font=("Arial", 12))

        scan_button = ttk.Button(toolbar, text="Scan Network", command=self.scan_network)
        scan_button.pack(side=tk.LEFT, padx=5, pady=5)

        reload_button = ttk.Button(toolbar, text="Reload Data", command=self.reload_data)
        reload_button.pack(side=tk.LEFT, padx=5, pady=5)

        save_button = ttk.Button(toolbar, text="Save", command=self.save_data)
        save_button.pack(side=tk.LEFT, padx=5, pady=5)

        help_button = ttk.Button(toolbar, text="Help", command=self.show_help)
        help_button.pack(side=tk.LEFT, padx=5, pady=5)

        exit_button = ttk.Button(toolbar, text="Exit", command=self.parent.quit)
        exit_button.pack(side=tk.LEFT, padx=5, pady=5)

        view_options = ["Network Tree", "Devices", "Grid View"]
        self.views = tk.StringVar(value=view_options[0])
        view_combo = ttk.Combobox(toolbar, values=view_options, textvariable=self.views, state="readonly")
        view_combo.current(0)
        view_combo.pack(side=tk.LEFT, padx=5, pady=5)

        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Create the main frame
        self.devices_table = ttk.Treeview(main_frame, selectmode="none")
        self.devices_table.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.devices_table["columns"] = ("device_name", "ip_address", "device_type", "software_version", "mac_address", "cpu_usage", "memory_usage")
        
        self.devices_table.heading("device_name", text="Device Name")
        self.devices_table.heading("ip_address", text="IP Address")
        self.devices_table.heading("device_type", text="Device Type")
        self.devices_table.heading("software_version", text="Software/Firmware Version")
        self.devices_table.heading("mac_address", text="MAC Address")
        self.devices_table.heading("cpu_usage", text="CPU Usage (%)")
        self.devices_table.heading("memory_usage", text="Memory Usage (%)")

        self.devices_table.column("device_name", width=150)
        self.devices_table.column("ip_address", width=100)
        self.devices_table.column("device_type", width=100)
        self.devices_table.column("software_version", width=200)
        self.devices_table.column("mac_address", width=150)
        self.devices_table.column("cpu_usage", width=100)
        self.devices_table.column("memory_usage", width=100)

        # Populate the devices table
        self.create_devices_table()

    def create_devices_table(self):
        # Clear the table
        for child in self.devices_table.get_children():
            self.devices_table.delete(child)

        # Add devices to the table
        for device in self.devices:
            device_name = device.get("device_name", "Unknown")
            ip_address = device.get("ip_address", "")
            device_type = device.get("device_type", "")
            software_version = device.get("software_version", "")
            mac_address = device.get("mac_address", "")
            cpu_usage = device.get("cpu_usage", "")
            memory_usage = device.get("memory_usage", "")
            
            self.devices_table.insert("", "end", values=(device_name, ip_address, device_type, software_version, mac_address, cpu_usage, memory_usage))

    def show_help(self):
        messagebox.showinfo("Help", "Please refer to the documentation for help.")

    def scan_network(self):
        self.device_detector.scan_devices()

    def reload_data(self):
        # Define the logic for reloading the data here
        pass

    def save_data(self):
        # Define the logic for saving data here
        messagebox.showinfo("Save Data", "Data has been saved successfully.")

    def run(self):
        self.parent.mainloop()

    def create_widgets(self):
        # Create a frame for the main content
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill="both", expand=True)

        # Create the IP address entry widget and add it to the main frame using pack
        self.ip_entry = tk.Entry(self.main_frame)
        self.ip_entry.pack(side=tk.TOP, padx=10, pady=10)

        # Create a frame for the device detector
        self.device_detector_frame = tk.Frame(self.main_frame)
        self.device_detector_frame.pack(padx=10, pady=10)

        # Create the devices detector object and display it
        self.device_detector = CustomDeviceDetector(self.device_detector_frame, timeout_value=3)

        # Create the device listbox and label
        self.device_listbox = tk.Listbox(self.main_frame)
        self.device_listbox.pack(side=tk.TOP, fill="both", expand=True, padx=10, pady=10)

        self.device_label = tk.Label(self.main_frame, text="Devices")
        self.device_label.pack(side=tk.TOP, padx=10, pady=10)

        # Create the "Show Devices" button
        self.show_devices_button = ttk.Button(self.main_frame, text="Show Devices", command=self.show_devices)
        self.show_devices_button.pack(side=tk.TOP, pady=5)

    def show_devices(self):
        # Clear the device listbox
        self.device_listbox.delete(0, tk.END)

        # Get the list of devices and add their IP addresses to the listbox
        devices = self.device_detector.devices
        for device in devices:
            self.device_listbox.insert(tk.END, device['ip'])

if __name__ == "__main__":
    root = tk.Tk()
    app = IoTShieldGUI(root)
    app.run()

