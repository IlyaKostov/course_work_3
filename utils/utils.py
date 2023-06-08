import json
from datetime import datetime


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


def separate_words(text):
    """
    Разделяем строку на слова и числовые значения
    :param text: название и номер карты/счета str
    :return: отдельно наименование карты/счета и их номер tuple
    """
    words = text.split()
    str_list = [word for word in words if word.isalpha()]
    int_list = [word for word in words if word.isdigit()]
    return ' '.join(str_list), ' '.join(int_list)


def hide_card_and_account(operation):
    """
    Скрываем номера счетов и карт
    :param operation: словарь с нужными ключами dict
    :return: замаскированные номера карт/счетов str
    """
    # извлекаем слова со строкой и числами для "from" и "to"
    from_str, from_int = separate_words(operation.get('from', ''))
    to_str, to_int = separate_words(operation.get('to', ''))

    # если "счет" есть в строке "from_str", то маскируем номер счета, если нет, то маскируем карту
    if 'счет' in from_str.lower():
        masked_from_int = f"**{from_int[-4:]}"
    else:
        masked_from_int = f"{from_int[:4]} {from_int[4:6]}** **** {from_int[-4:]}"

    # если "счет" есть в строке "to_str", то маскируем номер счета, если нет, то маскируем карту
    if 'счет' in to_str.lower():
        masked_to_int = f"**{to_int[-4:]}"
    else:                           #
        masked_to_int = f"{to_int[:4]} {to_int[4:6]}** **** {to_int[-4:]}"

    # проверяем наличие ключей, и выводим соответствующие замаскированные данные
    if 'from' in operation and 'to' in operation:
        return f'{from_str} {masked_from_int} -> {to_str} {masked_to_int}'
    elif 'to' in operation:
        return f'{to_str} {masked_to_int}'
    else:
        return "Номер карты/счета получателя не указан"
