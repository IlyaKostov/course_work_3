import os

from utils.utils import load_operations, sorted_by_date, last_executed_operations, date_converter, hide_card_and_account

PATH = os.path.join("operations.json")


def main():
    all_operations = load_operations(PATH)
    picked_out = sorted_by_date(all_operations)
    last_5_operations = last_executed_operations(picked_out)
    for operation in last_5_operations:
        print(f"{date_converter(operation)} {operation['description']}\n"
              f"{hide_card_and_account(operation)} \n"
              f"{operation['operationAmount']['amount']} {operation['operationAmount']['currency']['name']}\n")


if __name__ == '__main__':
    main()
