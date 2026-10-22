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



def show_operations(operations):
    """Печатает список всех операций."""
    if not operations:
        print("\nСписок операций пуст.")
        return

    print("\n{:<4} {:<8} {:<12} {:<15} {:<12}".format(
        "№", "Тип", "Сумма", "Категория", "Дата"))
    print("-" * 55)
    for i, op in enumerate(operations, 1):
        type_ru = "Доход" if op["type"] == "income" else "Расход"
        print("{:<4} {:<8} {:<12.2f} {:<15} {:<12}".format(
            i, type_ru, op["amount"], op["category"], op["date"]))


def show_balance(operations):
    """Печатает текущий баланс."""
    balance = calculate_balance(operations)
    print(f"\nТекущий баланс: {balance:.2f} руб.")


def print_menu():
    """Печатает главное меню."""
    print("\n===== Калькулятор личных финансов =====")
    print("1. Добавить доход")
    print("2. Добавить расход")
    print("3. Показать все операции")
    print("4. Показать баланс")
    print("0. Выход")
    print("========================================")


def input_operation(operations, op_type):
    """Запрашивает у пользователя данные и добавляет операцию."""
    try:
        amount = float(input("Введите сумму: "))
        category = input("Введите категорию: ").strip() or "Без категории"
        date_input = input("Введите дату (YYYY-MM-DD, Enter — сегодня): ").strip()
        add_operation(operations, op_type, amount, category,
                      date_input if date_input else None)
        save_operations(operations)
        print("Операция добавлена.")
    except ValueError as e:
        print(f"Ошибка ввода: {e}")


def main():
    """Точка входа: интерактивный цикл меню."""
    operations = load_operations()
    while True:
        print_menu()
        choice = input("Выберите пункт: ").strip()
        if choice == "1":
            input_operation(operations, "income")
        elif choice == "2":
            input_operation(operations, "expense")
        elif choice == "3":
            show_operations(operations)
        elif choice == "4":
            show_balance(operations)
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неверный пункт меню. Попробуйте снова.")


if __name__ == "__main__":
    main()
