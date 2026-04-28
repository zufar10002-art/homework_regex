from typing import Any, Dict, List


def filter_by_status(
    transactions: List[Dict[str, Any]], status: str
) -> List[Dict[str, Any]]:
    """Фильтрует транзакции по статусу."""
    result = []
    for t in transactions:
        state = t.get("state")
        if state is not None and isinstance(state, str):
            if state.upper() == status.upper():
                result.append(t)
    return result


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
