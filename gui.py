import tkinter as tk
import tkinter.ttk as ttk
from tkintertable import TableCanvas, TableModel
from color_swatch import color_swatch
import tkinter as tk
import sys
import os
from PIL import Image, ImageTk
from device_detector import DeviceDetector
from device_clustering import DeviceClustering
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, 'path/to/device_clustering'))

class Ui_IoTShield:
    def __init__(self, master, main_window):
        self.master = master
        self.main_window = main_window

        # call create_widgets() method
        self.create_buttons()

    def create_buttons(self):
        # check if main_window object is None
        if self.main_window is None:
            print("main_window object is None")
        else:
            # create button widget with command=self.main_window.scan_devices
            ttk.Button(button_bar, text="Scan Network", command=self.main_window.scan_devices, style="Cust.TButton").pack(side=tk.LEFT)

        self.root = root
        self.main_window = main_window
        self.create_widgets()
        self.main_window = None
        self.main_frame = tk.Frame(self.root)
        self.main_window = None  # add this line to initialize main_window attribute
        self.root.geometry("650x500")
        self.root.config(bg="#EFF0F1")
        self.create_buttons()
        self.root.bind("<Configure>", self._resize_handler)
        self._ui_ready = True

    def create_widgets(self):
        # Create a frame to hold the buttons
        button_bar = ttk.Frame(self.root, padding=10)
        button_bar.pack(fill=tk.X)

        # Create a button to scan the network for devices
        ttk.Button(button_bar, text="Scan Network", command=self.main_window.scan_devices).pack(side=tk.LEFT)

    def scan_devices(self):
        detector = DeviceDetector(timeout=1, num_threads=100)
        devices = detector.scan_devices()
        device_clustering = DeviceClustering(devices)
        clusters = device_clustering.cluster_devices()
        for device_type, device_list in clusters.items():
            print(f"{device_type}: {len(device_list)} devices")
        self.main_frame = tk.Frame(self.parent)

        self.main_frame.pack(side="top", fill="both", expand=True)

        # create a header frame
        self.header_frame = tk.Frame(self.main_frame)
        self.header_frame.pack(side="top", fill="both")

        # create a left frame
        self.left_frame = tk.Frame(self.main_frame, bg="white")
        self.left_frame.pack(side="left", fill="both")

        # create a right frame
        self.right_frame = tk.Frame(self.main_frame, bg="white")
        self.right_frame.pack(side="right", fill="both")

        # create a footer frame
        self.footer_frame = tk.Frame(self.main_frame)
        self.footer_frame.pack(side="bottom", fill="both")

        # create a label for the header
        self.header_label = tk.Label(self.header_frame, text="IoT Shield", font=("Arial Bold", 24))
        self.header_label.pack(padx=20, pady=20)

        # create a label for the left frame
        self.left_frame_label = tk.Label(self.left_frame, text="Device List", font=("Arial Bold", 14))
        self.left_frame_label.pack(padx=20, pady=20)

        # create a label for the right frame
        self.right_frame_label = tk.Label(self.right_frame, text="Device Info", font=("Arial Bold", 14))
        self.right_frame_label.pack(padx=20, pady=20)

        # create an image
        image = Image.open("images/loading.gif")
        self.loading_gif = ImageTk.PhotoImage(image)

        # initialize loading_popup attribute to None
        self.loading_popup = None


    def create_buttons(self):
        # Add a button for each device type
        button_bar = ttk.Frame(self.root)
        button_bar.pack(side="top", fill="x")

        for device_type in self.device_types:
            device_type_icon = self.device_clustering.get_device_type_icon(device_type)
            image = ImageTk.PhotoImage(Image.open(device_type_icon).resize((32, 32)))
            button = ttk.Button(button_bar, text=device_type, image=image,
                                compound="top", command=lambda dt=device_type: self.show_devices(dt))
            button.image = image
            button.pack(side="left", padx=10, pady=10)

        # Add a button to refresh the device list
        refresh_icon = "refresh_icon.png"
        refresh_image = ImageTk.PhotoImage(Image.open(refresh_icon).resize((32, 32)))
        refresh_button = ttk.Button(button_bar, text="Refresh", image=refresh_image, compound="top",
                                    command=self.refresh_devices)
        refresh_button.image = refresh_image
        refresh_button.pack(side="right", padx=10, pady=10)

    def _resize_handler(self, event):
        if self._ui_ready:
            self.left_frame.config(width=int(event.width/3))
            self.right_frame.config(width=int(event.width/3*2))

    def show_loading_popup(self):
        if self.loading_popup is not None:
            return
        self.loading_popup = tk.Toplevel(self)
        ...

        return

        # Create a Toplevel widget for the popup
        self.loading_popup = tk.Toplevel(self.parent.tk)
        self.loading_popup.title("Scanning devices...")
        self.loading_popup.geometry("400x200")

        # Create a Label to display the loading message
        message_label = tk.Label(self.loading_popup, text="Scanning all devices on the network which may take time...")
        message_label.pack(pady=10)

        # Center the popup on the parent window
        self.loading_popup.transient(self.parent.tk)
        x = self.parent.tk.winfo_rootx() + self.parent.tk.winfo_width() // 2 - self.loading_popup.winfo_width() // 2
        y = self.parent.tk.winfo_rooty() + self.parent.tk.winfo_height() // 2 - self.loading_popup.winfo_height() // 2
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
            data[index] = {"IP": device["ip"], "Hostname": device["hostname"], "MAC Address": device["mac"],
                           "Device Type": device["device_type"], "Last Seen": device["last_seen"]}

        model = TableModel()
        model.importDict(data)

        self.table.setModel(model)
        self.table.redrawTable()

    def create_buttons(self):
        # Create the buttons here
        button_bar = tk.Frame(self.main_frame)
        button_bar.pack(side="bottom", fill="x", pady=10)

        ttk.Button(button_bar, text="Scan Network", command=self.main_window.scan_devices, style="Cust.TButton").pack(
            side="left", padx=5)
        ttk.Button(button_bar, text="Logs", command=self.on_logs_button_clicked, style="Cust.TButton").pack(side="left",
                                                                                                            padx=5)
        ttk.Button(button_bar, text="Save to PDF", command=self.on_save_to_pdf_button_clicked,
                   style="Cust.TButton").pack(side="left", padx=5)
        ttk.Button(button_bar, text="Help", command=self.on_help_button_clicked, style="Cust.TButton").pack(side="left",
                                                                                                            padx=5)
        ttk.Button(button_bar, text="Exit", command=self.main_window.on_close, style="Cust.TButton").pack(side="right",
                                                                                                          padx=5)

        self.style = ttk.Style()
        self.style.configure("Cust.TButton", foreground=color_swatch["primary"], background=color_swatch["secondary"],
                             font=("Arial", 12, "bold"), width=20, height=2)

    def on_logs_button_clicked(self):
        # Implement the functionality you want when the Logs button is clicked
        print("Logs button clicked")

    def on_help_button_clicked(self):
        # Implement the functionality you want when the Help button is clicked
        print("Help button clicked")

    def on_save_to_pdf_button_clicked(self):
        # Add the code to save the data to a PDF file here
        print("Saving to PDF...")
