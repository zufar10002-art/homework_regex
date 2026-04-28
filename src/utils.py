import json
from typing import Any, Dict, List


def load_transactions_from_json(file_path: str) -> List[Dict[str, Any]]:
    """Загружает транзакции из JSON-файла."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
