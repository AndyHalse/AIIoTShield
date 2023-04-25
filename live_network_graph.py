import tkinter as tk

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from device_clustering import DeviceClustering
from device_detection import DeviceDetector

class LiveNetworkGraph(tk.Frame):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.graph = nx.Graph()

        # Initialize the Matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(8, 8), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def update_graph(self, data):
        """

        :param data:
        """
        # Clear the existing graph
        self.graph.clear()
        self.ax.clear()

        # Add nodes and edges based on the data
        for item in data:
            self.graph.add_node(item["name"])
            for connection in item["connections"]:
                self.graph.add_edge(item["name"], connection)

        # Draw the updated graph
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, ax=self.ax)
        self.canvas.draw()

    # Example usage:
    # data = [{"name": "Device 1", "connections": ["Device 2"]},
    #         {"name": "Device 2", "connections": ["Device 1", "Device 3"]},
    #         {"name": "Device 3", "connections": ["Device 2"]}]
    # live_network_graph = LiveNetworkGraph()
    # live_network_graph.update_graph(data)

    # Add at least one public method to the class
    def update_graph(self, data):
        # Add code to update the live network graph
        self.update_graph(data)
