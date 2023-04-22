import tkinter as tk
from color_swatch import colors

class IoTShieldApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("IoTShield")
        self.configure(bg=colors['background'])

        # Add your widgets and configure them using the colors dictionary
        self.label = tk.Label(self, text="Welcome to IoTShield", fg=colors['primary'], bg=colors['background'])
        self.label.pack(padx=20, pady=20)

        self.start_button = tk.Button(self, text="Start", fg=colors['success'], bg=colors['secondary'], command=self.start)
        self.start_button.pack(padx=10, pady=10)

        self.stop_button = tk.Button(self, text="Stop", fg=colors['error'], bg=colors['secondary'], command=self.stop)
        self.stop_button.pack(padx=10, pady=10)

    def start(self):
        print("Starting IoTShield...")

    def stop(self):
        print("Stopping IoTShield...")

if __name__ == "__main__":
    app = IoTShieldApp()
    app.mainloop()
