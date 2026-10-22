"""
Калькулятор личных финансов.
Консольное приложение для учёта доходов и расходов.
"""

import json
import os
from datetime import datetime

DATA_FILE = "finance_data.json"


def load_operations():
    """Загружает список операций из файла."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_operations(operations):
    """Сохраняет список операций в файл."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(operations, f, ensure_ascii=False, indent=2)


def add_operation(operations, op_type, amount, category, date=None):
    """
    Добавляет новую операцию.

    :param operations: список операций
    :param op_type: 'income' или 'expense'
    :param amount: сумма (положительное число)
    :param category: категория
    :param date: дата в формате YYYY-MM-DD (по умолчанию — сегодня)
    :return: обновлённый список операций
    """
    if op_type not in ("income", "expense"):
        raise ValueError("Тип операции должен быть 'income' или 'expense'")
    if amount <= 0:
        raise ValueError("Сумма должна быть положительной")

    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    else:
        datetime.strptime(date, "%Y-%m-%d")

    operations.append({
        "type": op_type,
        "amount": amount,
        "category": category,
        "date": date,
    })
    return operations


def calculate_balance(operations):
    """Возвращает текущий баланс: доходы минус расходы."""
    income = sum(op["amount"] for op in operations if op["type"] == "income")
    expense = sum(op["amount"] for op in operations if op["type"] == "expense")
    return income - expense
