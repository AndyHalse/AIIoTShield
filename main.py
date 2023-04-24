import logging
import tkinter as tk
from device_detection import DeviceDetector
from gui import Ui_IoTShield

# set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

class MainWindow:
    _last_child_ids = None

    def __init__(self):
        self.tk = tk.Tk()
        self.tk.title("IoT Shield")
        self.detector = DeviceDetector()
        self.loading_popup = None
        self.ui = Ui_IoTShield(self.tk, self)  # pass both the Tk object and the MainWindow object to Ui_IoTShield
        self.ui.setup_ui()
        # Set the close button event
        self.tk.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.ui.hide_loading_popup()
        self.destroy()

if __name__ == "__main__":
    # create a MainWindow object and start the tkinter main loop
    main_window = MainWindow()
    main_window.mainloop()
