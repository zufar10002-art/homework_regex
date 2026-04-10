import pandas as pd
from typing import List, Dict, Any


def read_csv_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Считывает финансовые операции из CSV-файла."""
    try:
        df = pd.read_csv(file_path, sep=';', encoding='utf-8')
        transactions = []
        for _, row in df.iterrows():
            trans = {
                "id": row.get("id"),
                "state": row.get("state"),
                "date": row.get("date"),
                "operationAmount": {
                    "amount": str(row.get("amount", "0")),
                    "currency": {
                        "name": row.get("currency_name", ""),
                        "code": row.get("currency_code", "")
                    }
                },
                "description": row.get("description", ""),
                "from": row.get("from", ""),
                "to": row.get("to", "")
            }
            transactions.append(trans)
        return transactions
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return []


def read_excel_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Считывает финансовые операции из Excel-файла."""
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        return df.to_dict(orient='records')
    except Exception as e:
        print(f"Error reading Excel: {e}")
        return []
