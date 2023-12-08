import mysql.connector
from datetime import datetime

class FinanceTracker:
    
    def __init__(self, db_host='localhost', db_user='root', db_password='password', db_name='finance_tracker'):
        self.conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        self.cursor = self.conn.cursor()
        self.initialize_database()

    def initialize_database(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS income (
                id INT AUTO_INCREMENT PRIMARY KEY,
                source VARCHAR(255),
                amount DOUBLE,
                date DATE)
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                amount DOUBLE,
                date DATE,
                category VARCHAR(255))
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS budgets (
                id INT AUTO_INCREMENT PRIMARY KEY,
                category VARCHAR(255),
                budget_limit DOUBLE)
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS savings_goals (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                target_amount DOUBLE,
                deadline DATE)
        ''')
        self.conn.commit()

    def add_income(self, source, amount, date=None):
        date = date or datetime.now().strftime('%Y-%m-%d')
        self.cursor.execute('INSERT INTO income (source, amount, date) VALUES (%s, %s, %s)', (source, amount, date))
        self.conn.commit()

    def add_expense(self, name, amount, date=None, category=None):
        date = date or datetime.now().strftime('%Y-%m-%d')
        category = category or "Uncategorized"
        self.cursor.execute('INSERT INTO expenses (name, amount, date, category) VALUES (%s, %s, %s, %s)', (name, amount, date, category))
        self.conn.commit()

    def create_budget(self, category, limit):
        limit = max(0, limit)
        self.cursor.execute('INSERT INTO budgets (category, budget_limit) VALUES (%s, %s)', (category, limit))
        self.conn.commit()
        budget_id = self.cursor.lastrowid
        print(f"Budget created - ID: {budget_id}, Category: {category}, Limit: {limit}")

    def add_savings_goal(self, name, target_amount, deadline):
        target_amount = max(0, target_amount)
        self.cursor.execute('INSERT INTO savings_goals (name, target_amount, deadline) VALUES (%s, %s, %s)', (name, target_amount, deadline))
        self.conn.commit()

    def track_spending(self):
        self.cursor.execute('SELECT SUM(amount) FROM expenses')
        total_expenses = self.cursor.fetchone()[0]
        print(f"Expenses: ${total_expenses}")

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

    def join_query(self):
        query = '''
        SELECT income.source, expenses.name AS expense_name, budgets.category, savings_goals.name AS savings_goal_name
        FROM income
        JOIN expenses ON income.id = expenses.income_id  -- Adjust the join condition here
        JOIN budgets ON expenses.category = budgets.category
        JOIN savings_goals ON budgets.id = savings_goals.budget_id
    '''
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        print("\nJoin Query Result:")
        for row in result:
            print(row)

    def delete_expense(self, expense_id):
        self.cursor.execute('SELECT id FROM expenses WHERE id=%s', (expense_id,))
        existing_expense = self.cursor.fetchone()
        if existing_expense:
            self.cursor.execute('DELETE FROM expenses WHERE id=%s', (expense_id,))
            self.conn.commit()
            print(f"Expense with ID {expense_id} deleted successfully.")
        else:
            print(f"Error: Expense with ID {expense_id} not found.")

    def update_budget_limit(self, budget_id, new_limit):
        self.cursor.execute('SELECT id FROM budgets WHERE id=%s', (budget_id,))
        existing_budget_ids = [row[0] for row in self.cursor.fetchall()]
        print(f"Existing Budget IDs: {existing_budget_ids}")
        self.cursor.execute('SELECT id FROM budgets WHERE id=%s', (budget_id,))
        existing_budget = self.cursor.fetchone()

        if existing_budget:
            new_limit = max(0, new_limit)
            self.cursor.execute('UPDATE budgets SET budget_limit=%s WHERE id=%s', (new_limit, budget_id))
            self.conn.commit()
            print(f"Budget with ID {budget_id} updated with a new limit: {new_limit}")
        else:
            print(f"Error: Budget with ID {budget_id} not found.")

    def __del__(self):
        self.conn.close()


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
def cli():
    finance_tracker = FinanceTracker()

    while True:
        print("\n===== Finance Tracker Menu =====")
        print("1. Enter Income")
        print("2. Enter Expense")
        print("3. Create Budget")
        print("4. Enter Savings Goal")
        print("5. Track Spending")
        print("6. Generate Financial Report")
        print("7. Join Query")
        print("8. Delete Expense")
        print("9. Update Budget Limit")
        print("0. Exit")

        choice = input("Enter your choice (0-9): ")

        try:
            choice = int(choice)
        except ValueError:
            print("Error: Please enter a valid number between 0 and 9.")
            continue

        if choice == 1:
            source = input("Enter income source: ")
            try:
                amount = float(input("Enter income amount: "))
            except ValueError:
                print("Error: Please enter a valid numeric amount.")
                continue
            finance_tracker.add_income(source, amount)
        elif choice == 2:
            name = input("Enter expense name: ")
            try:
                amount = float(input("Enter expense amount: "))
            except ValueError:
                print("Error: Please enter a valid numeric amount.")
                continue
            date = input("Enter expense date (YYYY-MM-DD): ")
            category = input("Enter expense category: ")
            finance_tracker.add_expense(name, amount, date, category)
        elif choice == 3:
            category = input("Enter budget category: ")
            try:
                limit = float(input("Enter budget limit: "))
            except ValueError:
                print("Error: Please enter a valid numeric limit.")
                continue
            finance_tracker.create_budget(category, limit)
        elif choice == 4:
            name = input("Enter savings goal name: ")
            try:
                target_amount = float(input("Enter savings goal target amount: "))
            except ValueError:
                print("Error: Please enter a valid numeric target amount.")
                continue
            deadline = input("Enter savings goal deadline (YYYY-MM-DD): ")
            finance_tracker.add_savings_goal(name, target_amount, deadline)
        elif choice == 5:
            finance_tracker.track_spending()
        elif choice == 6:
            finance_tracker.generate_financial_report()
        elif choice == 7:
            finance_tracker.join_query()
        elif choice == 8:
            try:
                expense_id = int(input("Enter expense ID to delete: "))
            except ValueError:
                print("Error: Please enter correct numeric expense ID.")
                continue
            finance_tracker.delete_expense(expense_id)
        elif choice == 9:
            try:
                budget_id = int(input("Enter budget ID to update: "))
                new_limit = float(input("Enter new budget limit: "))
            except ValueError:
                print("Error: Please enter correct numeric values for budget ID and limit.")
                continue
            finance_tracker.update_budget_limit(budget_id, new_limit)
        elif choice == 0:
            print("Exiting Finance Tracker. BYE!")
            break
        else:
            print("Error: Invalid. Please enter number between 0 & 9.")


if __name__ == "__main__":
    cli()
    
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
    finance_tracker.join_query()  

    
    expense_to_delete_id = 1  
    finance_tracker.delete_expense(expense_to_delete_id)

    budget_to_update_id = 1  
    new_budget_limit = 400
    finance_tracker.update_budget_limit(budget_to_update_id, new_budget_limit)
