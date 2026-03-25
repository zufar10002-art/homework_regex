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


def load_transactions_from_csv(file_path: str) -> List[Dict[str, Any]]:
    """Загружает транзакции из CSV-файла (заглушка)."""
    print("Программа: Функция загрузки из CSV пока не реализована.")
    return []


def load_transactions_from_xlsx(file_path: str) -> List[Dict[str, Any]]:
    """Загружает транзакции из XLSX-файла (заглушка)."""
    print("Программа: Функция загрузки из XLSX пока не реализована.")
    return []


def filter_by_status(
    transactions: List[Dict[str, Any]], status: str
) -> List[Dict[str, Any]]:
    """Фильтрует транзакции по статусу."""
    return [
        t for t in transactions
        if t.get("state", "").upper() == status.upper()
    ]


def sort_by_date(
    transactions: List[Dict[str, Any]], ascending: bool = True
) -> List[Dict[str, Any]]:
    """Сортирует транзакции по дате."""
    return sorted(
        transactions,
        key=lambda x: x.get("date", ""),
        reverse=not ascending
    )


def filter_rub_only(
    transactions: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Оставляет только рублевые транзакции."""
    result = []
    for t in transactions:
        op_amount = t.get("operationAmount", {})
        currency = op_amount.get("currency", {}).get("code", "")
        if currency == "RUB":
            result.append(t)
    return result


def format_date(date_str: str) -> str:
    """Форматирует дату из ISO в DD.MM.YYYY."""
    if not date_str:
        return "Дата неизвестна"
    try:
        parts = date_str.split("T")[0].split("-")
        return f"{parts[2]}.{parts[1]}.{parts[0]}"
    except (IndexError, AttributeError):
        return "Дата неизвестна"


def mask_card_number(card_str: str) -> str:
    """Маскирует номер карты или счета."""
    if not card_str:
        return "Нет данных"
    if "Счет" in card_str:
        numbers = ''.join(filter(str.isdigit, card_str))
        if len(numbers) >= 4:
            return f"Счет **{numbers[-4:]}"
        return card_str
    parts = card_str.split()
    if len(parts) >= 2:
        card_num = parts[-1]
        if len(card_num) >= 16:
            masked = f"{card_num[:4]} {card_num[4:6]}** **** {card_num[-4:]}"
            return f"{parts[0]} {masked}"
    return card_str


def main():
    """Основная логика программы."""
    print("Программа: Привет! Добро пожаловать в программу работы "
          "с банковскими транзакциями.")

    print("\nВыберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Пользователь: ").strip()

    if choice == "1":
        print("Программа: Для обработки выбран JSON-файл.")
        transactions = load_transactions_from_json("data/operations.json")
    elif choice == "2":
        print("Программа: Для обработки выбран CSV-файл.")
        transactions = load_transactions_from_csv("data/transactions.csv")
    elif choice == "3":
        print("Программа: Для обработки выбран XLSX-файл.")
        transactions = load_transactions_from_xlsx(
            "data/transactions_excel.xlsx"
        )
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
        print("Программа: Найдено", found_count,
              "транзакций по слову", search_word)

    print("\nПрограмма: Распечатываю итоговый список транзакций...\n")
    print(f"Всего банковских операций в выборке: {len(filtered)}")

    for t in filtered:
        date = format_date(t.get("date", ""))
        description = t.get("description", "")
        op_amount = t.get("operationAmount", {})
        amount = op_amount.get("amount", "")
        currency = op_amount.get("currency", {}).get("code", "")
        from_info = mask_card_number(t.get("from", ""))
        to_info = mask_card_number(t.get("to", ""))

        print(f"\n{date} {description}")
        if from_info != "Нет данных":
            print(f"{from_info} -> {to_info}")
        else:
            print(f"Кому: {to_info}")
        print(f"Сумма: {amount} {currency}")


if __name__ == "__main__":
    main()
