import csv
import datetime
import os

from Expense import *


class ExpenseService:
    def __init__(self):
        self.expenses = []
        self.budget = 0

    def add_expense(self, expense: Expense):
        print("Adding expense...")
        if isinstance(expense, Expense):
            expense_dict = {'date': expense.date, 'category': expense.category, 'amount': expense.amount,
                            'description': expense.description}
            self.expenses.append(expense_dict)

    def get_expenses(self):
        print("Viewing expenses...")
        for exp in self.expenses:
            if exp['date'] is not None and exp['category'] is not None and exp['amount'] is not None and exp[
                'description'] is not None:
                print(exp)
            else:
                print("in-complete record")

    def user_input(self):
        try:
            amount = float(input('Enter amount : '))
            category = input('Enter category : ')
            description = input('Enter description : ')
            date = datetime.date.today()
        except ValueError as message:
            return None
        expense_user_input = Expense(amount=amount, category=category, description=description, date=date)
        return expense_user_input

    def set_budget(self):
        self.budget = float(input('Enter budget : '))

    def track_budget(self, old_expenses):
        print("Tracking budget...")
        total_amount = 0
        for exp in self.expenses:
            total_amount += exp['amount']
        for exp in old_expenses:
            total_amount += exp['amount']
        if total_amount > self.budget:
            print('You have exceeded your budget!')
        else:
            print('You have {} left for the month'.format(self.budget - total_amount))

    def save_expenses(self):
        filename = 'expenses.csv'
        write_header = not os.path.exists(filename) or os.path.getsize(filename) == 0

        with open(filename, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['date', 'category', 'amount', 'description'])

            # Only write header if file doesn't exist or is empty
            if not write_header:
                writer.writeheader()

            for expense in self.expenses:
                writer.writerow({
                    'date': expense['date'].isoformat(),
                    'category': expense['category'],
                    'amount': expense['amount'],
                    'description': expense['description']
                })

        print(f"Expenses appended to {filename}")

    def load_expenses(self):
        filename = 'expenses.csv'
        prev_expenses = []

        if not os.path.exists(filename) or os.path.getsize(filename) == 0:
            print("File is empty. No records to load.")
            return prev_expenses

        with open(filename, mode='r', newline='') as file:
            reader = csv.DictReader(file)

            for row in reader:
                # Skip empty rows or rows missing 'date'
                if not row or 'date' not in row or row['date'] in ('', 'date'):
                    continue

                try:
                    row['date'] = datetime.date.fromisoformat(row['date'])
                    row['amount'] = float(row['amount'])
                    prev_expenses.append(row)
                except (ValueError, KeyError) as e:
                    print(f"Skipping malformed row: {row} | Error: {e}")

        print(f"Loaded {len(prev_expenses)} expenses")
        return prev_expenses

    def menu(self):
        e = ExpenseService()
        while True:
            print("\n--- Expense Tracker Menu ---")
            print("1. Add expense")
            print("2. View expenses")
            print("3. Track budget")
            print("4. Save expenses")
            print("5. Exit")
            choice = input("Enter your choice (1-5): ")
            if choice == '1':
                n = int(input("Enter number of expenses : "))
                for i in range(n):
                    expense = e.user_input()
                    if expense:
                        e.add_expense(expense)
                    else:
                        print('No expense recorded')
            elif choice == '2':
                e.get_expenses()
            elif choice == '3':
                old_expenses = e.load_expenses()
                if old_expenses:
                    for exp in old_expenses:
                        e.add_expense(exp)
                e.set_budget()
                e.track_budget(old_expenses)
            elif choice == '4':
                old_expenses = e.load_expenses()
                if old_expenses:
                    for exp in old_expenses:
                        e.add_expense(exp)
                e.save_expenses()
            elif choice == '5':
                print("Exiting... Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == '__main__':
    service = ExpenseService()
    service.menu()