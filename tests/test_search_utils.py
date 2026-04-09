"""
Тесты для модуля search_utils.
"""

from src.search_utils import search_transactions


def test_search_transactions_found():
    data = [
        {"description": "Перевод организации"},
        {"description": "Перевод с карты на карту"},
        {"description": "Открытие вклада"},
    ]
    result = search_transactions(data, "Перевод")
    assert len(result) == 2


def test_search_transactions_not_found():
    data = [{"description": "Перевод организации"}]
    result = search_transactions(data, "Платеж")
    assert result == []


def test_search_transactions_empty_data():
    result = search_transactions([], "Перевод")
    assert result == []


def test_search_transactions_empty_search():
    data = [{"description": "Перевод организации"}]
    result = search_transactions(data, "")
    assert result == []


def test_search_transactions_case_insensitive():
    data = [{"description": "Перевод организации"}]
    result = search_transactions(data, "перевод")
    assert len(result) == 1
