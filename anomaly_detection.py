    # Function to calculate byte rates
    def calculate_byte_rates(self, devices):
        byte_rates = {}
        for device in devices:
            byte_rates[device["ip"]] = {"in": random.randint(
                1000, 10000), "out": random.randint(1000, 10000)}
        return byte_rates

    def detect_anomalies(devices, byte_rates):
        if not isinstance(devices, list):
            raise TypeError("devices must be a list")
        if not isinstance(byte_rates, dict):
            raise TypeError("byte_rates must be a dictionary")
            
        # Perform anomaly detection on byte_rates data
        anomalies = []

        # Look up byte rates by device IP address
        for i, device in enumerate(devices):
            ip = device["ip"]
            if byte_rates.get(ip, {}).get("in", 0) > 10000 or byte_rates.get(ip, {}).get("out", 0) > 10000:
                anomalies.append(i)

        return anomalies