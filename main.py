import logging
import tkinter as tk
from tkinter import messagebox

from device_detector import DeviceDetector

from gui import Ui_IoTShield

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("AI Cyber IoT Shield")

        # Create a menu bar
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # Create a File menu
        file_menu = tk.Menu(menubar)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.on_close)

        # Create a Help menu
        help_menu = tk.Menu(menubar)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.on_help_button_clicked)

        # Create a Logs menu
        logs_menu = tk.Menu(menubar)
        menubar.add_cascade(label="Logs", menu=logs_menu)
        logs_menu.add_command(label="Show Logs", command=self.on_logs_button_clicked)

        # Create a main frame for the window
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill="both", expand=True)

        # Create an instance of DeviceDetector and Ui_IoTShield
        self.detector = DeviceDetector(user_agent="Mozilla/5.0")
        self.ui = Ui_IoTShield(main_window=self, reload_data_func=self.reload_data)
        self.ui.pack(side="top", fill="both", expand=True)

        print("Scanning for devices...")
        self.update_device_table(self.detector.scan_devices())

    def update_device_table(self, devices):
        self.ui.device_table.delete(*self.ui.device_table.get_children())
        for device in devices:
            self.ui.device_table.insert("", "end", values=(
                device["hostname"], device["ip"], device["mac"], device["device_type"], device["last_seen"]))

    # rest of the code stays the same

    def on_close(self):
        try:
            self.ui.destroy()
        except tk.TclError:
            pass
        self.destroy()

    def reload_data(self):
        try:
            self.ui.progressBar["value"] = 0
            self.ui.header_label.config(text="Scanning for devices...")
            self.ui.reload_data_button.config(state="disabled")
            self.detector = DeviceDetector()
            devices = self.detector.scan_devices()
            self.update_device_table(devices)
            self.ui.header_label.config(text="Data reloaded")
            logging.info("Data reloaded successfully")
            self.ui.reload_data_button.config(state="normal")
        except Exception as e:
            self.ui.header_label.config(text="Failed to reload data")
            logging.error(f"Failed to reload data: {str(e)}")
            messagebox.showerror("Error", f"Failed to reload data: {str(e)}")

    def update_table(self, devices):
        print(f"Found {len(devices)} devices.")
        self.ui.tableWidget.delete(*self.ui.tableWidget.get_children())
        for device in devices:
            icon = DataProcessing.get_device_icon(device["device_type"])
            self.ui.tableWidget.insert("", "end", values=(
                device["ip"], device["mac"], device["hostname"], device["device_type"], device["last_seen"], icon))

    def on_help_button_clicked(self):
        messagebox.showinfo("Help", "This is the AI Cyber IoT Shield application. It automatically detects and identifies all LAN/WAN network devices, including IoT, IP CCTV cameras, routers, IP telephones, wireless mobiles, Amazon Echo devices, Apple Not devices, and any other wireless devices that could be vulnerable to outside hackers. The application displays IP address, device name, device type, device software/firmware version number, MAC address, CPU data, memory data, and any other relevant information.")

    def on_logs_button_clicked(self):
        with open('app.log', 'r') as file:
            logs = file.read()
            messagebox.showinfo("Logs", logs)

if __name__ == "__main__":
    main_window = MainWindow()
    main_window.title("AI Cyber IoT Shield")
    main_window.iconbitmap("assets/logo.ico")
    main_window.resizable(False, False)
    main_window.protocol("WM_DELETE_WINDOW", main_window.on_close)

    # Add a frame to the main window
    main_window.frame = tk.Frame(main_window)
    main_window.frame.pack(side="top", fill="both", expand=True)

    # Create an instance of DeviceDetector and Ui_IoTShield
    main_window.detector = DeviceDetector(timeout=1)

    main_window.ui = Ui_IoTShield(
        main_window=main_window, reload_data_func=main_window.reload_data)

    main_window.ui.pack(side="top", fill="both", expand=True)

    print("Scanning for devices...")
    main_window.update_device_table(main_window.detector.scan_devices())

    main_window.mainloop()
