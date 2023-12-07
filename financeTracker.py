import sqlite3
from datetime import datetime

class FinanceTracker:
    def __init__(self, db_name='finance_tracker.db'):
        
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

       
        self.initialize_database()

    def initialize_database(self):
       self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS income (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT,
                amount REAL,
                date DATE)
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                amount REAL,
                date DATE,
                category TEXT)
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT,
                limit REAL)
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS savings_goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                target_amount REAL,
                deadline DATE)
        ''')

    def add_income(self, source, amount, date=None):
        date = date or datetime.now().strftime('%Y-%m-%d')
        self.cursor.execute('INSERT INTO income (source, amount, date) VALUES (?, ?, ?)', (source, amount, date))
        self.conn.commit()

    def add_expense(self, name, amount, date=None, category=None):
        date = date or datetime.now().strftime('%Y-%m-%d')
        category = category or "Uncategorized"
        self.cursor.execute('INSERT INTO expenses (name, amount, date, category) VALUES (?, ?, ?, ?)', (name, amount, date, category))
        self.conn.commit()

    def create_budget(self, category, limit):
        limit = max(0, limit) 
        self.cursor.execute('INSERT INTO budgets (category, limit) VALUES (?, ?)', (category, limit))
        self.conn.commit()

    def add_savings_goal(self, name, target_amount, deadline):
        target_amount = max(0, target_amount)  
        self.cursor.execute('INSERT INTO savings_goals (name, target_amount, deadline) VALUES (?, ?, ?)', (name, target_amount, deadline))
        self.conn.commit()
    
    def track_spending(self):
        self.cursor.execute('SELECT SUM(amount) FROM expenses')
        total_expenses = self.cursor.fetchone()[0]
        print(f"Total Expenses: ${total_expenses}")

    def generate_financial_report(self):
        print("\nFinancial Summary:")
        self.cursor.execute('SELECT * FROM income')
        income_data = self.cursor.fetchall()
        print("Income:")
        for income in income_data:
            print(f"{income[1]}: ${income[2]} on {income[3]}")

        self.cursor.execute('SELECT * FROM expenses')
        expenses_data = self.cursor.fetchall()
        print("\nExpenses:")
        for expense in expenses_data:
            print(f"{expense[1]}: ${expense[2]} on {expense[3]} ({expense[4]})")

class Income:
    def __init__(self, finance_tracker):
        self.finance_tracker = finance_tracker

    def add_income(self, source, amount, date=None):
        self.finance_tracker.add_income(source, amount, date)


class Expenses:
    def __init__(self, finance_tracker):
        self.finance_tracker = finance_tracker

    def add_expense(self, name, amount, date=None, category=None):
        self.finance_tracker.add_expense(name, amount, date, category)


class Budgets:
    def __init__(self, finance_tracker):
        self.finance_tracker = finance_tracker

    def create_budget(self, category, limit):
        self.finance_tracker.create_budget(category, limit)


class SavingsGoals:
    def __init__(self, finance_tracker):
        self.finance_tracker = finance_tracker

    def add_savings_goal(self, name, target_amount, deadline):
        self.finance_tracker.add_savings_goal(name, target_amount, deadline)


if __name__ == "__main__":
    
    finance_tracker = FinanceTracker()

    income_manager = Income(finance_tracker)
    income_manager.add_income("Salary", 3000)

    expenses_manager = Expenses(finance_tracker)
    expenses_manager.add_expense("Rent", 1200, category="Housing")
    expenses_manager.add_expense("Groceries", 200, category="Groceries")

    budgets_manager = Budgets(finance_tracker)
    budgets_manager.create_budget("Groceries", 300)

    savings_manager = SavingsGoals(finance_tracker)
    savings_manager.add_savings_goal("Emergency Fund", 5000, "2023-12-31")

    finance_tracker.track_spending()
    finance_tracker.generate_financial_report()
