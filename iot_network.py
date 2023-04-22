# iot_network.py
class IoTNetwork:
    # ...

    def send_data(self, device_id, data):
        device = self.get_device(device_id)
        if device and not device.blocked:  # Check if the device is blocked before allowing data transfer
            device.send_data(data)
        else:
            print(f"Data transfer blocked for device {device_id}")

    def receive_data(self, device_id):
        device = self.get_device(device_id)
        if device and not device.blocked:  # Check if the device is blocked before allowing data transfer
            return device.receive_data()
        else:
            print(f"Data transfer blocked for device {device_id}")
            return None
