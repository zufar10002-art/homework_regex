"""
Модуль для подсчета количества операций по категориям.
"""

from typing import Any, Dict, List


def count_operations_by_category(
    data: List[Dict[str, Any]], categories: List[str]
) -> Dict[str, int]:
    """
    Подсчитывает количество операций в каждой категории.

    Args:
        data: Список словарей с данными о транзакциях.
        categories: Список категорий для подсчета.

    Returns:
        Словарь, где ключ — категория, значение — количество операций.
    """
    if not data or not categories:
        return {category: 0 for category in categories}

    # Собираем все описания
    descriptions = [item.get("description", "") for item in data]

    # Создаем счетчик для каждой категории
    result = {}
    for category in categories:
        count = sum(
            1 for desc in descriptions if category.lower() in desc.lower()
        )
        result[category] = count

    return result
