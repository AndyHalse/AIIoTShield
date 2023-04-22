import matplotlib.pyplot as plt


def plot_pie_chart(normal_count, abnormal_count, output_path):
    """

    :param normal_count:
    :param abnormal_count:
    :param output_path:
    """
    labels = ["Normal Devices", "Abnormal Devices"]
    sizes = [normal_count, abnormal_count]
    colors = ["#5a17d6", "#a37cf0"]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")

    plt.savefig(output_path)

# Example usage:
# plot_pie_chart(90, 10, "pie_chart.png")
