import os
import tkinter as tk
from tkinter import ttk

from device_detection import DeviceDetector


class IoTShieldGUI:
    def __init__(self, title="IoT Shield", width=800, height=600):
        self.title = title
        self.width = width
        self.height = height
        self.saved_data = []
        self.device_detector = None

        try:
            self.device_detector = DeviceDetector()
        except Exception as e:
            print(f"Error initializing DeviceDetector: {e}")

        # create root window and set its title and geometry
        self.root = tk.Tk()
        self.root.title(self.title)
        self.root.geometry(f"{self.width}x{self.height}")

        # create menu bar
        self.menu_bar = tk.Menu(self.root)

        # create file menu and its options
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Save", command=self.save_data)
        file_menu.add_command(label="Reload", command=self.reload_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # create edit menu and its options
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Scan Network", command=self.scan_network)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # create help menu and its options
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="Help", command=self.show_help)
        help_menu.add_command(label="About", command=self.show_about)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

        # configure root window with menu bar
        self.root.config(menu=self.menu_bar)

        # create toolbar
        self.toolbar = tk.Frame(self.root)
        scan_button = ttk.Button(self.toolbar, text="Scan", command=self.scan_network)
        scan_button.pack(side=tk.LEFT, padx=2, pady=2)

        device_label = ttk.Label(self.toolbar, text="Devices:")
        device_label.pack(side=tk.LEFT, padx=2, pady=2)

        self.device_combobox = ttk.Combobox(self.toolbar, values=self.get_device_models())
        self.device_combobox.pack(side=tk.LEFT, padx=2, pady=2)

        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # create table frame
        self.table_frame = ttk.Frame(self.root)
        self.create_table()
        self.table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def initialize_widgets(self):
        try:
            self.create_table()

            # create menu bar
            self.menu_bar = tk.Menu(self.root)

            # create file menu and its options
            file_menu = tk.Menu(self.menu_bar, tearoff=0)
            file_menu.add_command(label="Save", command=self.save_data)
            file_menu.add_command(label="Reload", command=self.reload_data)
            file_menu.add_separator()
            file_menu.add_command(label="Exit", command=self.root.quit)
            self.menu_bar.add_cascade(label="File", menu=file_menu)

            # create edit menu and its options
            edit_menu = tk.Menu(self.menu_bar, tearoff=0)
            edit_menu.add_command(label="Scan Network", command=self.scan_network)
            self.menu_bar.add_cascade(label="Edit", menu=edit_menu)

            # create help menu and its options
            help_menu = tk.Menu(self.menu_bar, tearoff=0)
            help_menu.add_command(label="Help", command=self.show_help)
            help_menu.add_command(label="About", command=self.show_about)
            self.menu_bar.add_cascade(label="Help", menu=help_menu)

            # configure root window with menu bar
            self.root.config(menu=self.menu_bar)

            # create toolbar
            self.toolbar = tk.Frame(self.root)
            scan_button = ttk.Button(self.toolbar, text="Scan", command=self.scan_network)
            scan_button.pack(side=tk.LEFT, padx=2, pady=2)

            device_label = ttk.Label(self.toolbar, text="Devices:")
            device_label.pack(side=tk.LEFT, padx=2, pady=2)

            self.device_combobox = ttk.Combobox(self.toolbar, values=self.get_device_models())
            self.device_combobox.pack(side=tk.LEFT, padx=2, pady=2)

            self.toolbar.pack(side=tk.TOP, fill=tk.X)

            self.table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        except Exception as e:
            print(f"Error initializing widgets: {e}")

    def create_table(self):
        try:
            # Define the columns for the table
            columns = ("IP Address", "MAC Address", "Device Manufacturer", "Device Name")

            # Create the table with the defined columns
            self.table = ttk.Treeview(self.table_frame, columns=columns, show="headings")

            # Set column headings
            for col in columns:
                self.table.heading(col, text=col)

            # Pack the table into the UI
            self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Retrieve device data and store it in saved_data
            devices = self.device_detector.detect()
            self.saved_data = devices

            # Populate the table with device data
            for device in devices:
                self.table.insert("", tk.END, values=[device.ip_address, device.mac_address, device.vendor_name, device.model])

            # Populate a combobox with unique device types
            self.device_combobox['values'] = self.get_device_models()

            # Pack the table into the UI again
            self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        except Exception as e:
            print(f"Error creating table: {e}")

    def get_device_models(self):
        devices = self.device_detector.detect()
        return [device.model for device in devices]

    def scan_network(self):
        try:
            if self.device_detector is None:
                print("DeviceDetector is not available.")
                return

            devices = self.device_detector.detect()
            for device in devices:
                self.table.insert("", tk.END, values=[device.ip_address, device.mac_address, device.vendor_name, device.model])
            self.saved_data += devices
            self.device_combobox['values'] = self.get_device_models()
            self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        except Exception as e:
            print(f"Error scanning network: {e}")
            
    def save_data(self):
        directory = "/Users/andyhalse/AI Cyber Solutions Projects/AICyberIotShield/saved_data"
        if not os.path.exists(directory):
            os.makedirs(directory)
        filename = "data.txt"
        with open(directory + filename, "w") as file:
            for record in self.saved_data:
                file.write(f"{record}\n")
        print(f"Data saved to {directory}{filename}")

    def show_help(self):
        print("""
        Available Commands:
        -------------------
        1. start: Start collecting data
        2. sinset-block-start: Stop collecting data
        3. save: Save collected data to file
        4. clear: Clear collected data
        5. help: Show available commands
        6. exit: Exit the application
        """)

    def show_about(self):
        import tkinter.messagebox as messagebox
        info = "IoTShieldGUI App"
        messagebox.showinfo("About IoTShieldGUI", info)

    def reload_data(self):
        print("Reload data")

    def run(self):
        try:
            self.initialize_widgets()
            self.root.mainloop()
        except Exception as e:
            print(f"Error: {e}")
