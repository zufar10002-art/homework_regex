"""
Главный модуль программы для работы с банковскими транзакциями.
"""

import json
from typing import Any, Dict, List

from src.search_utils import search_transactions


def load_transactions_from_json(file_path: str) -> List[Dict[str, Any]]:
    """Загружает транзакции из JSON-файла."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def filter_by_status(
    transactions: List[Dict[str, Any]], status: str
) -> List[Dict[str, Any]]:
    """Фильтрует транзакции по статусу."""
    return [
        t for t in transactions
        if t.get("state", "").upper() == status.upper()
    ]


def main():
    """Основная логика программы."""
    print("Программа: Привет! Добро пожаловать в программу работы "
          "с банковскими транзакциями.")

    # Загрузка данных
    transactions = load_transactions_from_json("data/operations.json")
    if not transactions:
        print("Программа: Не удалось загрузить данные.")
        return

    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Пользователь: ").strip()

    if choice == "1":
        print("Программа: Для обработки выбран JSON-файл.")
    else:
        print("Программа: В данной версии поддерживается только JSON-файл.")
        return

    # Фильтрация по статусу
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

    # Поиск по описанию
    print("\nПрограмма: Отфильтровать список транзакций по определенному "
          "слову в описании? Да/Нет")
    search_choice = input("Пользователь: ").strip().lower()

    if search_choice in ["да", "yes", "y"]:
        search_word = input("Программа: Введите слово для поиска: ").strip()
        filtered = search_transactions(filtered, search_word)
        print(f"Программа: Найдено {len(filtered)} транзакций по слову "
              f"\"{search_word}\".")

    # Вывод результатов
    print("\nПрограмма: Распечатываю итоговый список транзакций...\n")
    print(f"Всего банковских операций в выборке: {len(filtered)}")

    for t in filtered:
        date_str = t.get("date", "")
        if date_str:
            date = date_str.split("T")[0]
        else:
            date = "Дата неизвестна"

        description = t.get("description", "Описание отсутствует")
        operation_amount = t.get("operationAmount", {})
        amount = operation_amount.get("amount", "0")
        currency = operation_amount.get("currency", {}).get("code", "")
        from_info = t.get("from", "Нет данных")
        to_info = t.get("to", "Нет данных")

        print(f"\n{date} {description}")
        print(f"От: {from_info}")
        print(f"Кому: {to_info}")
        print(f"Сумма: {amount} {currency}")


if __name__ == "__main__":
    main()
