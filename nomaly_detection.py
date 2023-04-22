import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

class AnomalyDetection:

    def __init__(self):
        self.scaler = StandardScaler()
        self.model = IsolationForest(contamination=0.1)

    def fit(self, X):

        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled)

    def predict(self, X):

        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)

    def detect_anomalies(self, data):

        X = np.array([d["features"] for d in data])
        y_pred = self.predict(X)
        anomalies = [d for d, y in zip(data, y_pred) if y == -1]
        return anomalies

# Example usage:
# data = [{"name": "Device 1", "features": [1, 2, 3]},
#         {"name": "Device 2", "features": [4, 5, 6]},
#         {"name": "Device 3", "features": [7, 8, 9]}]
# ad = AnomalyDetection()
# ad.fit([d["features"] for d in data])
# anomalies = ad.detect_anomalies(data)
