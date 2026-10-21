import json
import os
from datetime import datetime

DATA_FILE = "operations.json"

def load_operations():
    """Загружает операции из файла."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            print("Ошибка чтения файла данных. Начинаем с чистого листа.")
            return []
    return []

def save_operations(operations):
    """Сохраняет операции в файл."""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(operations, f, ensure_ascii=False, indent=4)
    except IOError:
        print("Ошибка сохранения данных!")

def add_operation(operations):
    """Добавляет новую операцию (доход или расход)."""
    print("\n--- Добавление новой операции ---")
    while True:
        op_type = input("Тип операции (доход/расход): ").strip().lower()
        if op_type in ['доход', 'расход']:
            break
        print("Неверный тип. Пожалуйста, введите 'доход' или 'расход'.")

    try:
        amount = float(input("Сумма: "))
        if amount <= 0:
            print("Сумма должна быть положительной.")
            return operations
    except ValueError:
        print("Неверная сумма. Введите число.")
        return operations

    category = input("Категория (например, Еда, Транспорт, Зарплата): ").strip()
    date_str = input("Дата (ГГГГ-ММ-ДД) или нажмите Enter для сегодня: ").strip()

    if not date_str:
        date_str = datetime.now().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print("Неверный формат даты. Используйте ГГГГ-ММ-ДД.")
            return operations

    operation = {
        "type": op_type,
        "amount": amount,
        "category": category,
        "date": date_str
    }

    operations.append(operation)
    save_operations(operations)
    print("Операция успешно добавлена!")
    return operations

def show_operations(operations):
    """Выводит список всех операций."""
    print("\n--- Список операций ---")
    if not operations:
        print("Список операций пуст.")
        return

    for i, op in enumerate(operations, 1):
        sign = "+" if op['type'] == 'доход' else "-"
        print(f"{i}. [{op['date']}] {sign}{op['amount']:.2f} руб. - {op['category']} ({op['type']})")

def show_balance(operations):
    """Рассчитывает и выводит текущий баланс."""
    print("\n--- Текущий баланс ---")
    income = sum(op['amount'] for op in operations if op['type'] == 'доход')
    expense = sum(op['amount'] for op in operations if op['type'] == 'расход')
    balance = income - expense

    print(f"Доходы:   +{income:.2f} руб.")
    print(f"Расходы:  -{expense:.2f} руб.")
    print(f"Баланс:   {balance:.2f} руб.")

def main():
    """Основная функция с интерактивным меню."""
    operations = load_operations()
    print("Добро пожаловать в Калькулятор личных финансов!")

    while True:
        print("\n--- Меню ---")
        print("1. Добавить операцию")
        print("2. Посмотреть все операции")
        print("3. Посмотреть баланс")
        print("4. Выход")

        choice = input("Выберите действие (1-4): ").strip()

        if choice == '1':
            operations = add_operation(operations)
        elif choice == '2':
            show_operations(operations)
        elif choice == '3':
            show_balance(operations)
        elif choice == '4':
            print("Выход из программы. До свидания!")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
