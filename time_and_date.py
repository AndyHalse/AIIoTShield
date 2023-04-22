from datetime import datetime


def current_time_and_date():
    """

    :return:
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
