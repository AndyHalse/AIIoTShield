from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest


def create_dataframe():
    """

    """
    # Implement a function to create a pandas DataFrame with network data
    pass


def cluster_devices(df):
    """

    :param df:
    :return:
    """
    kmeans = KMeans(n_clusters=2)
    df['cluster'] = kmeans.fit_predict(df)
    return df


def detect_anomalies(df):
    """

    :param df:
    :return:
    """
    isolation_forest = IsolationForest()
    df['anomaly'] = isolation_forest.fit_predict(df)
    return df
