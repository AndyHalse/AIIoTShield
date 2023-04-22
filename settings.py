# settings.py

# Application settings
APP_NAME = "IoTShield"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "An application to protect and manage IoT devices."

# MQTT settings
MQTT_BROKER = "mqtt.example.com"
MQTT_PORT = 1883
MQTT_USERNAME = "username"
MQTT_PASSWORD = "password"
MQTT_KEEPALIVE = 60
MQTT_TOPIC = "IoTShield"

# Database settings
DATABASE_URI = "sqlite:///iotshield.db"
DATABASE_NAME = "iotshield"

# Security settings
API_KEY = "your_api_key_here"
SECRET_KEY = "your_secret_key_here"

# Email settings
EMAIL_HOST = "smtp.example.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_USERNAME = "username"
EMAIL_PASSWORD = "password"
EMAIL_FROM = "noreply@example.com"

# Logging settings
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = "iotshield.log"

# Device settings
MAX_DEVICES = 100
