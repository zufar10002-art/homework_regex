"""
Главный модуль программы для работы с банковскими транзакциями.
"""

import os

from src.utils import load_transactions_from_json
from src.file_processing import (
    read_csv_transactions,
    read_excel_transactions
)
from src.processing_utils import (
    filter_by_status,
    sort_by_date,
    filter_rub_only,
    format_date
)
from src.masks import mask_card_number
from src.search_utils import search_transactions


def main():
    """Основная логика программы."""
    print("Программа: Привет! Добро пожаловать в программу работы "
          "с банковскими транзакциями.")

    root_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(root_dir, "data")

    print("\nВыберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Пользователь: ").strip()

    if choice == "1":
        print("Программа: Для обработки выбран JSON-файл.")
        file_path = os.path.join(data_dir, "operations.json")
        transactions = load_transactions_from_json(file_path)
    elif choice == "2":
        print("Программа: Для обработки выбран CSV-файл.")
        file_path = os.path.join(data_dir, "transactions.csv")
        transactions = read_csv_transactions(file_path)
    elif choice == "3":
        print("Программа: Для обработки выбран XLSX-файл.")
        file_path = os.path.join(data_dir, "transactions_excel.xlsx")
        transactions = read_excel_transactions(file_path)
    else:
        print("Программа: Неверный выбор. Завершение работы.")
        return

    if not transactions:
        print("Программа: Не удалось загрузить данные.")
        return

    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]

    while True:
        print("\nПрограмма: Введите статус, по которому необходимо "
              "выполнить фильтрацию.")
        print(f"Доступные для фильтровки статусы: "
              f"{', '.join(valid_statuses)}")
        status_input = input("Пользователь: ").strip().upper()

        if status_input in valid_statuses:
            print(f"Программа: Операции отфильтровываются по статусу "
                  f"\"{status_input}\".")
            filtered = filter_by_status(transactions, status_input)
            break
        else:
            print(f"Программа: Статус операции \"{status_input}\" недоступен.")

    if not filtered:
        print("Программа: Не найдено ни одной транзакции, подходящей под "
              "ваши условия фильтрации")
        return

    print("\nПрограмма: Отсортировать операции по дате? Да/Нет")
    sort_choice = input("Пользователь: ").strip().lower()

    if sort_choice in ["да", "yes", "y"]:
        print("Программа: Отсортировать по возрастанию или по убыванию?")
        order = input("Пользователь: ").strip().lower()
        if order in ["по возрастанию", "возрастанию", "asc"]:
            filtered = sort_by_date(filtered, ascending=True)
            print("Программа: Операции отсортированы по дате (возрастание).")
        elif order in ["по убыванию", "убыванию", "desc"]:
            filtered = sort_by_date(filtered, ascending=False)
            print("Программа: Операции отсортированы по дате (убывание).")
        else:
            print("Программа: Неверный ввод. Сортировка не применена.")

    print("\nПрограмма: Выводить только рублевые транзакции? Да/Нет")
    rub_choice = input("Пользователь: ").strip().lower()

    if rub_choice in ["да", "yes", "y"]:
        filtered = filter_rub_only(filtered)
        print("Программа: Отфильтрованы только рублевые транзакции.")

    print("\nПрограмма: Отфильтровать список транзакций по определенному "
          "слову в описании? Да/Нет")
    search_choice = input("Пользователь: ").strip().lower()

    if search_choice in ["да", "yes", "y"]:
        search_word = input("Программа: Введите слово для поиска: ").strip()
        filtered = search_transactions(filtered, search_word)
        found_count = len(filtered)
        print(f"Программа: Найдено {found_count} транзакций по слову "
              f"\"{search_word}\".")

    print("\nПрограмма: Распечатываю итоговый список транзакций...\n")
    print(f"Всего банковских операций в выборке: {len(filtered)}")

    for t in filtered:
        date = format_date(t.get("date", ""))
        description = t.get("description", "Описание отсутствует")
        op_amount = t.get("operationAmount", {})
        amount = op_amount.get("amount", "0")
        currency_data = op_amount.get("currency", {})
        if isinstance(currency_data, dict):
            currency = currency_data.get("code", "")
        else:
            currency = ""
        from_info = mask_card_number(t.get("from", ""))
        to_info = mask_card_number(t.get("to", ""))

        print(f"\n{date} {description}")
        if from_info and from_info != "Нет данных":
            print(f"{from_info} -> {to_info}")
        else:
            print(to_info)
        print(f"Сумма: {amount} {currency}")


if __name__ == "__main__":
    main()
