"""
Тесты для модуля main.
"""

import json
from unittest.mock import mock_open, patch

from src.main import filter_by_status, load_transactions_from_json


def test_load_transactions_from_json_success():
    """Тест успешной загрузки JSON."""
    mock_data = [{"id": 1}, {"id": 2}]
    mock_file = mock_open(read_data=json.dumps(mock_data))

    with patch("builtins.open", mock_file):
        result = load_transactions_from_json("fake_path.json")

    assert result == mock_data


def test_load_transactions_from_json_file_not_found():
    """Тест при отсутствии файла."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = load_transactions_from_json("fake_path.json")

    assert result == []


def test_load_transactions_from_json_invalid_json():
    """Тест при невалидном JSON."""
    mock_file = mock_open(read_data="not json")

    with patch("builtins.open", mock_file):
        result = load_transactions_from_json("fake_path.json")

    assert result == []


def test_filter_by_status():
    """Тест фильтрации по статусу."""
    data = [
        {"state": "EXECUTED"},
        {"state": "CANCELED"},
        {"state": "EXECUTED"},
        {"state": "PENDING"},
    ]
    result = filter_by_status(data, "EXECUTED")
    assert len(result) == 2
    assert all(t["state"] == "EXECUTED" for t in result)


def test_filter_by_status_case_insensitive():
    """Тест регистронезависимой фильтрации."""
    data = [{"state": "executed"}, {"state": "CANCELED"}]
    result = filter_by_status(data, "EXECUTED")
    assert len(result) == 1
    assert result[0]["state"] == "executed"


def test_filter_by_status_no_match():
    """Тест при отсутствии совпадений."""
    data = [{"state": "CANCELED"}, {"state": "PENDING"}]
    result = filter_by_status(data, "EXECUTED")
    assert result == []
