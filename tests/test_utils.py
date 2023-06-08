import json

import pytest

from utils.utils import sorted_by_date, last_executed_operations, date_converter, separate_words, hide_card_and_account, \
    load_operations


@pytest.fixture
def operations_fixture():
    operations = [
        {"state": "EXECUTED", "date": "2019-08-26T10:50:58"},
        {"state": "EXECUTED", "date": "2018-03-23T10:45:06"},
        {"state": "EXECUTED", "date": "2018-08-19T04:27:37"},
        {},
        {"state": "CANCELED", "date": "2018-10-14T08:21:33"},
        {"state": "EXECUTED", "date": "2018-04-14T19:35:28"},
        {"state": "EXECUTED", "date": "2018-08-06T16:22:54"},
    ]
    return operations


def test_load_operations_file_not_found_error():
    with pytest.raises(FileNotFoundError):
        load_operations("")


def test_sorted_by_date(operations_fixture):
    result = [
        {"state": "EXECUTED", "date": "2019-08-26T10:50:58"},
        {"state": "CANCELED", "date": "2018-10-14T08:21:33"},
        {"state": "EXECUTED", "date": "2018-08-19T04:27:37"},
        {"state": "EXECUTED", "date": "2018-08-06T16:22:54"},
        {"state": "EXECUTED", "date": "2018-04-14T19:35:28"},
        {"state": "EXECUTED", "date": "2018-03-23T10:45:06"},
        {},
    ]
    assert sorted_by_date(operations_fixture) == result
    assert sorted_by_date([]) == []


def test_last_executed_operations(operations_fixture):
    result = [
        {"state": "EXECUTED", "date": "2019-08-26T10:50:58"},
        {"state": "EXECUTED", "date": "2018-03-23T10:45:06"},
        {"state": "EXECUTED", "date": "2018-08-19T04:27:37"},
        {"state": "EXECUTED", "date": "2018-04-14T19:35:28"},
        {"state": "EXECUTED", "date": "2018-08-06T16:22:54"}
    ]
    assert last_executed_operations(operations_fixture) == result
    assert last_executed_operations([]) == []


def test_date_converter():
    assert date_converter({"date": "2019-08-26T10:50:58"}) == "26.08.2019"
    assert date_converter({"date": "2018-08-06T16:22:54.643491"}) == "06.08.2018"


def test_date_converter_key_error():
    with pytest.raises(KeyError):
        date_converter({})


def test_separate_words():
    assert separate_words("Maestro 1596837868705199") == ("Maestro", "1596837868705199")
    assert separate_words("Счет 2724852958655") == ("Счет", "2724852958655")
    assert separate_words("Счет") == ("Счет", "")
    assert separate_words("4839759223") == ("", "4839759223")
    assert separate_words("") == ("", "")


def test_hide_card_and_account():
    operation = {"from": "МИР 4878656375033856", "to": "Maestro 6890749237669619"}
    assert hide_card_and_account(operation) == "МИР 4878 65** **** 3856 -> Maestro 6890 74** **** 9619"

    operation = {"to": "Maestro 6890749237669619"}
    assert hide_card_and_account(operation) == "Maestro 6890 74** **** 9619"

    operation = {"to": "Счет 34616199494072692721"}
    assert hide_card_and_account(operation) == "Счет **2721"

    operation = {"from": "Счет 59956820797131895975", "to": "Счет 34616199494072692721"}
    assert hide_card_and_account(operation) == "Счет **5975 -> Счет **2721"
    assert hide_card_and_account({}) == "Номер карты/счета получателя не указан"

    operation = {"from": "Счет 59956820797131895975"}
    assert hide_card_and_account(operation) == "Номер карты/счета получателя не указан"
