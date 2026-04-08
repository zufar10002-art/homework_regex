"""
Module for reading financial transactions from CSV and Excel files.
"""

from typing import Any, Dict, List

import pandas as pd


def read_csv_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Reads financial transactions from a CSV file.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        List[Dict[str, Any]]: List of dictionaries containing transaction data.
                              Returns empty list on error.
    """
    try:
        df = pd.read_csv(file_path, sep=';', encoding='utf-8')
        return df.to_dict(orient='records')
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return []


def read_excel_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Reads financial transactions from an Excel file.

    Args:
        file_path (str): Path to the Excel file.

    Returns:
        List[Dict[str, Any]]: List of dictionaries containing transaction data.
                              Returns empty list on error.
    """
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        return df.to_dict(orient='records')
    except Exception as e:
        print(f"Error reading Excel: {e}")
        return []
