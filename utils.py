import json
import os
from datetime import datetime

PATH = os.path.join("operations.json")


def load_operations(path):
    """
    Загрузка данных из файла
    :param path: путь к файлу
    :return: список операций json
    """
    with open(path) as file:
        operations = json.load(file)
    return operations



