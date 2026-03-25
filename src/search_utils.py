"""
Модуль для поиска транзакций по описанию с использованием
регулярных выражений.
"""

import re
from typing import Any, Dict, List


def search_transactions(
    data: List[Dict[str, Any]], search_str: str
) -> List[Dict[str, Any]]:
    """
    Ищет транзакции, в описании которых содержится заданная строка.

    Args:
        data: Список словарей с данными о транзакциях.
        search_str: Строка для поиска в описании.

    Returns:
        Список транзакций, у которых в description есть искомая строка.
    """
    if not data or not search_str:
        return []

    pattern = re.compile(re.escape(search_str), re.IGNORECASE)
    result = []

    for transaction in data:
        description = transaction.get("description", "")
        if pattern.search(description):
            result.append(transaction)

    return result
