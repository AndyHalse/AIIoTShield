import tkinter as tk
import tkinter.ttk as ttk
from tkintertable import TableCanvas, TableModel
from color_swatch import color_swatch
import tkinter as tk
from PIL import Image, ImageTk

class Ui_IoTShield:
    _ui_ready = False

    def __init__(self, parent):
        self.parent = parent

    def setup_ui(self):
        self.parent.tk.geometry("650x500")
        self.parent.tk.config(bg="#EFF0F1")

        self.create_widgets()

        self.parent.tk.bind("<Configure>", self._resize_handler)
        self._ui_ready = True

    def create_widgets(self):
        # create a main frame
        self.main_frame = tk.Frame(self.parent.tk)
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

    def _resize_handler(self, event):
        if self._ui_ready:
            self.left_frame.config(width=int(event.width/3))
            self.right_frame.config(width=int(event.width/3*2))

    def show_loading_popup(self):
        if self.loading_popup is not None:
            # The popup is already displayed
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

    def setup_ui(self):
        # Define the UI elements here
        self.create_buttons()

    def on_save_to_pdf_button_clicked(self):
        # Add the code to save the data to a PDF file here
        print("Saving to PDF...")
