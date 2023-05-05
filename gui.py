import os
import tkinter as tk
from tkinter import messagebox, ttk

import pandas as pd
from device_detector import DeviceDetector

import device_detection
from color_swatch import color_swatch

class IoTShieldGUI:
    def __init__(self):
        # devices can be a list of device objects or a string pointing to a CSV file
        self.device_detector = DeviceDetector(str(network))
        self.title = "IoT Shield GUI"
        self.width = 800
        self.height = 600
        
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
        edit_menu.add_command(label="Refresh List", command=self.refresh_list)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # create help menu and its options
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="Help", command=self.show_help)
        help_menu.add_command(label="About", command=self.show_about)

        # configure root window with menu bar
        self.root.config(menu=self.menu_bar)

        # create toolbar
        self.toolbar = ttk.Frame(self.root)
        scan_button = ttk.Button(self.toolbar, text="Refresh List", command=self.refresh_list)
        scan_button.pack(side=tk.LEFT, padx=2, pady=2)

        device_label = ttk.Label(self.toolbar, text="Devices:")
        device_label.pack(side=tk.LEFT, padx=2, pady=2)

        self.device_combobox = ttk.Combobox(self.toolbar, values=self.device_detector.get_device_models())
        self.device_combobox.pack(side=tk.LEFT, padx=2, pady=2)

        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # create table frame
        self.table_frame = ttk.Frame(self.root)
        self.create_table()
        self.table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # initialize device detector
        self.refresh_list()
        
        
    def refresh_list(self):
        self.device_detector.scan_network()

class SaveData:

    def __init__(self, saved_data):
        self.saved_data = saved_data

    def save_data(self):
        try:
            directory = "saved_data"
            if not os.path.exists(directory):
                os.makedirs(directory)

            filename = "data.txt"
            file_path = os.path.join(directory, filename)

            with open(file_path, "w") as file:
                for record in self.saved_data:
                    file.write(f"{record}\n")
            
            print(f"Data saved to {file_path}")

        except Exception as e:
            print(f"Error saving data: {e}")

            saved_data = ['record1', 'record2', 'record3']
            saver = SaveData(saved_data)
            saver.save_data()


    def initialize_widgets(self):
        try:
            # define create_table() before it is called
            def create_table():
                pass

            create_table()

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

            # define self.table_frame before using pack() on it
            self.table_frame = tk.Frame(self.root)
            self.table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        except Exception as e:
            print(f"Error initializing widgets: {e}")

    def create_table(self):
        columns = ("IP Address", "MAC Address", "Vendor Name", "Device Type", "OS", "OS Version", "Open Ports", "Subnet Info", "DHCP Info", "Network Info", "Security Info")
        try:
            # Create the table with the defined columns
            self.table = ttk.Treeview(self.table_frame, columns=columns, show="headings")
            # Set column headings
            for col in columns:
                self.table.heading(col, text=col)
            # Pack the table into the UI
            self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Populate a combobox with unique device types
            self.device_combobox = ttk.Combobox(self.table_frame)
            self.device_combobox['values'] = self.get_device_models()

        except Exception as e:
            print(f"Error creating table: {e}") 


    def show_help(self):
            print("""
            Available Commands:
            -------------------
            1. start: Start collecting data
            2. stop: Stop collecting data
            3. save: Save collected data to file
            4. clear: Clear collected data
            5. help: Show available commands
            6. exit: Exit the application
                    """)

    def reload_data(self):
        df = pd.read_csv('data.csv') # load data from csv
        self.data_table.delete(*self.data_table.get_children()) # clear existing data
        for index, row in df.iterrows():
            self.data_table.insert('', 'end', text=index, values=row.tolist()) # insert new data into table

    def show_about(self):
        import tkinter.messagebox as messagebox
        info = "IoTShieldGUI App"
        messagebox.showinfo("About IoTShieldGUI", info)

    def run(self):
        try:
            self.initialize_widgets()
            self.root.mainloop()
        except tk.TclError as e:
            messagebox.showerror("Error", f"{e}")
            # alternatively, log the error to a file:
            # with open("error.log", "a") as f:
            #     print(f"Error: {e}", file=f)
            

