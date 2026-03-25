"""
Тесты для модуля category_utils.
"""

from src.category_utils import count_operations_by_category


def test_count_operations_by_category():
    """Тест подсчета операций по категориям."""
    data = [
        {"description": "Перевод организации"},
        {"description": "Перевод с карты на карту"},
        {"description": "Открытие вклада"},
        {"description": "Перевод организации"},
    ]
    categories = ["Перевод", "Вклад"]
    result = count_operations_by_category(data, categories)
    assert result["Перевод"] == 3
    assert result["Вклад"] == 1


def test_count_operations_empty_data():
    """Тест с пустым списком транзакций."""
    result = count_operations_by_category([], ["Перевод", "Вклад"])
    assert result["Перевод"] == 0
    assert result["Вклад"] == 0


def test_count_operations_empty_categories():
    """Тест с пустым списком категорий."""
    data = [{"description": "Перевод организации"}]
    result = count_operations_by_category(data, [])
    assert result == {}


def test_count_operations_case_insensitive():
    """Тест регистронезависимого подсчета."""
    data = [
        {"description": "Перевод организации"},
        {"description": "перевод с карты"},
    ]
    categories = ["Перевод"]
    result = count_operations_by_category(data, categories)
    assert result["Перевод"] == 2


def test_count_operations_no_match():
    """Тест, когда нет совпадений."""
    data = [{"description": "Открытие вклада"}]
    categories = ["Перевод", "Платеж"]
    result = count_operations_by_category(data, categories)
    assert result["Перевод"] == 0
    assert result["Платеж"] == 0
