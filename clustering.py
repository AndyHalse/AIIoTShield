import sklearn.cluster


class DeviceClustering:

    def __init__(self, n_clusters=2):
        """
        Initialize DeviceClustering model with the specified number of clusters.

        :param n_clusters: The number of clusters to form. Default is 2.
        """
        self.model = sklearn.cluster.KMeans(n_clusters=n_clusters)

    def fit(self, X):
        """
        Fit the KMeans model to the input data.

        :param X: Input data.
        """
        self.model.fit(X)

    def predict(self, X):
        """
        Predict the cluster labels for the input data.

        :param X: Input data.
        :return: The predicted cluster labels.
        """
        return self.model.predict(X)

    def group_devices(self, data, np):
        """
        Group the devices based on their features using the KMeans model.

        :param data: A list of dictionaries containing device names and their features.
        :param np: Numpy module.
        :return: A dictionary with cluster labels as keys and the list of devices belonging to that cluster as values.
        """
        X = np.array([d["features"] for d in data])
        y_pred = self.predict(X)
        groups = {i: [] for i in range(self.model.n_clusters)}

        for device, group in zip(data, y_pred):
            groups[group].append(device)

        return groups

# Example usage:
# data = [{"name": "Device 1", "features": [1, 2, 3]},
#         {"name": "Device 2", "features": [4, 5, 6]},
#         {"name": "Device 3", "features": [7, 8, 9]}]
# clustering = DeviceClustering(n_clusters=2)
# clustering.fit(data)
# groups = clustering.group_devices(data)
