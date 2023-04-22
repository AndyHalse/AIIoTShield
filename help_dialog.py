from PyQt6.QtWidgets import QDialog

class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Help")

        # Implement the layout and content for the help dialog
        
    def open_help(self):
        self.exec_()
