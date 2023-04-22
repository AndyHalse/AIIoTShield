# device.py
class IoTDevice:
    def __init__(self, device_id, device_type):
        self.device_id = device_id
        self.device_type = device_type
        self.blocked = False  # Add this attribute to store the device's connection status

    def block_device(self):
        self.blocked = True

    def unblock_device(self):
        self.blocked = False
