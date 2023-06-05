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


def sorted_by_date(operations):
    """
    Сортируем список операций
    :param operations: список операций list
    :return: отсортированный список операций list
    """
    # Создаем 2 списка операций (имеющих и не имеющих ключ 'date')
    valid_operations = [operation for operation in operations if 'date' in operation]
    invalid_operations = [operation for operation in operations if 'date' not in operation]

    # сортируем по ключу 'date'
    valid_operations = sorted(valid_operations, key=lambda item: item['date'], reverse=True)

    # добавляем в конец списка операции без ключа 'date'
    return valid_operations + invalid_operations


def last_executed_operations(operations):
    """
    Получаем 5 последних, выполненных, операций
    :param operations: список операций list
    :return: последние 5 выполненных операций list
    """
    return [operation for operation in operations if operation.get('state') == 'EXECUTED'][:5]


def date_converter(operation):
    """
    Конвертируем дату в нужный нам формат
    :param operation: словарь с имеющимся ключом dict
    :return: дата в нужном нам формате str
    """
    return datetime.fromisoformat(operation['date']).strftime('%d.%m.%Y')


