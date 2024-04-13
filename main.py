import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()

# Create expenses table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS expenses
                (id INTEGER PRIMARY KEY,
                amount REAL,
                category TEXT,
                date TEXT)''')
conn.commit()


def add_expense(amount, category):
    now = datetime.now()
    date = now.strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)", (amount, category, date))
    conn.commit()
    messagebox.showinfo("Success", "Expense added successfully!")


def view_expenses():
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()

    for expense in expenses:
        print(expense)


def generate_summary():
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    summary = cursor.fetchall()

    df = pd.DataFrame(summary, columns=['Category', 'Total Amount'])

    plt.figure(figsize=(8, 6))
    plt.pie(df['Total Amount'], labels=df['Category'], autopct='%1.1f%%', startangle=140)
    plt.title('Expense Distribution by Category')
    plt.axis('equal')
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.bar(df['Category'], df['Total Amount'], color='skyblue')
    plt.xlabel('Category')
    plt.ylabel('Total Amount')
    plt.title('Expense Distribution by Category')
    plt.xticks(rotation=45)
    plt.show()


def submit_form():
    amount = float(entry_amount.get())
    category = entry_category.get()
    add_expense(amount, category)


root = tk.Tk()
root.title("Expense Tracker")

frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

label_amount = tk.Label(frame, text="Amount:")
label_amount.grid(row=0, column=0, sticky='e')

entry_amount = tk.Entry(frame)
entry_amount.grid(row=0, column=1)

label_category = tk.Label(frame, text="Category:")
label_category.grid(row=1, column=0, sticky='e')

entry_category = tk.Entry(frame)
entry_category.grid(row=1, column=1)

submit_button = tk.Button(frame, text="Submit", command=submit_form)
submit_button.grid(row=2, columnspan=2)

view_button = tk.Button(root, text="View Expenses", command=view_expenses)
view_button.pack(pady=10)

summary_button = tk.Button(root, text="Generate Summary", command=generate_summary)
summary_button.pack(pady=10)

sample_data = [
    (100, 'Food'),
    (50, 'Transportation'),
    (80, 'Entertainment'),
    (30, 'Shopping'),
]

for data in sample_data:
    add_expense(data[0], data[1])

root.mainloop()

conn.close()
