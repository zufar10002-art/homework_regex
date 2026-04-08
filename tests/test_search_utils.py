"""
Тесты для модуля search_utils.
"""

from src.search_utils import search_transactions

def test_search_transactions_found():
    """Тест поиска существующей строки."""
    data = [
        {"description": "Перевод организации"},
        {"description": "Перевод с карты на карту"},
        {"description": "Открытие вклада"},
    ]
    result = search_transactions(data, "Перевод")
    assert len(result) == 2
    assert "Перевод" in result[0]["description"]


def test_search_transactions_not_found():
    """Тест поиска несуществующей строки."""
    data = [
        {"description": "Перевод организации"},
        {"description": "Перевод с карты на карту"},
    ]
    result = search_transactions(data, "Платеж")
    assert result == []


def test_search_transactions_empty_data():
    """Тест с пустым списком транзакций."""
    result = search_transactions([], "Перевод")
    assert result == []


def test_search_transactions_empty_search():
    """Тест с пустой строкой поиска."""
    data = [{"description": "Перевод организации"}]
    result = search_transactions(data, "")
    assert result == []


def test_search_transactions_case_insensitive():
    """Тест регистронезависимого поиска."""
    data = [{"description": "Перевод организации"}]
    result = search_transactions(data, "перевод")
    assert len(result) == 1
