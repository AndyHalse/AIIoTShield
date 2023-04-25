from flask import Flask, render_template

from device_detector import DeviceDetector
from device_clustering import DeviceClustering

# Replace the network_prefixes list with your actual network prefixes
network_prefixes = [
    {"prefix": "192.168.0", "start": 1, "end": 254},
    # Add more network prefixes if necessary
]

# Initialize the detector with the network_prefixes
detector = DeviceDetector(network_prefixes)

# Flask app
app = Flask(__name__)


@app.route("/")
def index():
    devices = detector.scan_devices()
    return render_template("index.html", devices=devices)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
