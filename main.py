from device_detection import DeviceDetector
from gui import Ui_IoTShield
import tkinter as tk


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.network = DeviceDetector(timeout=1, num_threads=100) # add timeout and num_threads here
        self.ui = Ui_IoTShield(self.root, self, self.network)
        self.ui.create_widgets()
        self.root.mainloop()


if __name__ == "__main__":
    main_window = MainWindow()
