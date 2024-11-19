import os
import sqlite3
from cryptography.fernet import Fernet
from tkinter import Tk, Label, Button, Entry, messagebox, Listbox, END
import logging

# Logging setup
logging.basicConfig(filename="banking.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Encryption setup
key_file = "key.key"
if not os.path.exists(key_file):
    key = Fernet.generate_key()
    with open(key_file, "wb") as keyfile:
        keyfile.write(key)
else:
    with open(key_file, "rb") as keyfile:
        key = keyfile.read()
cipher = Fernet(key)

# Database setup
db_file = "banking.db"
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts (
    id TEXT PRIMARY KEY,
    balance REAL NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id TEXT NOT NULL,
    amount REAL NOT NULL,
    FOREIGN KEY(account_id) REFERENCES accounts(id)
)
""")
conn.commit()

# Add account
def add_account(account_id, balance):
    try:
        encrypted_id = cipher.encrypt(account_id.encode()).decode()
        cursor.execute("INSERT INTO accounts (id, balance) VALUES (?, ?)", (encrypted_id, balance))
        conn.commit()
        logging.info(f"Account {account_id} added successfully.")
    except sqlite3.IntegrityError:
        logging.error(f"Account {account_id} already exists.")
        messagebox.showerror("Error", "Account already exists.")

# Deposit
def deposit(account_id, amount):
    try:
        encrypted_id = cipher.encrypt(account_id.encode()).decode()
        cursor.execute("SELECT balance FROM accounts WHERE id = ?", (encrypted_id,))
        result = cursor.fetchone()
        if result:
            new_balance = result[0] + amount
            cursor.execute("UPDATE accounts SET balance = ? WHERE id = ?", (new_balance, encrypted_id))
            cursor.execute("INSERT INTO transactions (account_id, amount) VALUES (?, ?)", (encrypted_id, amount))
            conn.commit()
            logging.info(f"Deposited {amount} to account {account_id}. New balance: {new_balance}")
        else:
            raise ValueError("Account not found.")
    except Exception as e:
        logging.error(f"Error during deposit: {e}")
        messagebox.showerror("Error", str(e))

# Withdraw
def withdraw(account_id, amount):
    try:
        encrypted_id = cipher.encrypt(account_id.encode()).decode()
        cursor.execute("SELECT balance FROM accounts WHERE id = ?", (encrypted_id,))
        result = cursor.fetchone()
        if result:
            if result[0] >= amount:
                new_balance = result[0] - amount
                cursor.execute("UPDATE accounts SET balance = ? WHERE id = ?", (new_balance, encrypted_id))
                cursor.execute("INSERT INTO transactions (account_id, amount) VALUES (?, ?)", (encrypted_id, -amount))
                conn.commit()
                logging.info(f"Withdrew {amount} from account {account_id}. New balance: {new_balance}")
            else:
                raise ValueError("Insufficient funds.")
        else:
            raise ValueError("Account not found.")
    except Exception as e:
        logging.error(f"Error during withdrawal: {e}")
        messagebox.showerror("Error", str(e))

# Check balance
def check_balance(account_id):
    try:
        encrypted_id = cipher.encrypt(account_id.encode()).decode()
        cursor.execute("SELECT balance FROM accounts WHERE id = ?", (encrypted_id,))
        result = cursor.fetchone()
        if result:
            balance = result[0]
            logging.info(f"Checked balance for account {account_id}: {balance}")
            return balance
        else:
            raise ValueError("Account not found.")
    except Exception as e:
        logging.error(f"Error during balance check: {e}")
        messagebox.showerror("Error", str(e))

# Predict balance using Simple Moving Average
def predict_balance(account_id, n=5):
    try:
        encrypted_id = cipher.encrypt(account_id.encode()).decode()
        cursor.execute("SELECT amount FROM transactions WHERE account_id = ? ORDER BY id DESC LIMIT ?", (encrypted_id, n))
        transactions = cursor.fetchall()
        if transactions and len(transactions) >= n:
            average_transaction = sum(amount for (amount,) in transactions) / n
            current_balance = check_balance(account_id)
            predicted_balance = current_balance + average_transaction
            logging.info(f"Predicted balance for account {account_id}: {predicted_balance}")
            return predicted_balance
        else:
            raise ValueError("Not enough transaction data.")
    except Exception as e:
        logging.error(f"Error during balance prediction: {e}")
        messagebox.showerror("Error", str(e))

# GUI
def gui():
    def handle_deposit():
        account_id = account_entry.get()
        amount = float(amount_entry.get())
        deposit(account_id, amount)
        messagebox.showinfo("Success", f"Deposited {amount} to account {account_id}.")

    def handle_withdraw():
        account_id = account_entry.get()
        amount = float(amount_entry.get())
        withdraw(account_id, amount)
        messagebox.showinfo("Success", f"Withdrew {amount} from account {account_id}.")

    def handle_check_balance():
        account_id = account_entry.get()
        balance = check_balance(account_id)
        messagebox.showinfo("Balance", f"Account {account_id} balance: {balance}")

    def handle_predict_balance():
        account_id = account_entry.get()
        predicted = predict_balance(account_id, 5)
        messagebox.showinfo("Prediction", f"Predicted balance: {predicted}")

    # Tkinter setup
    root = Tk()
    root.title("Banking Management System")

    Label(root, text="Account ID:").grid(row=0, column=0)
    account_entry = Entry(root)
    account_entry.grid(row=0, column=1)

    Label(root, text="Amount:").grid(row=1, column=0)
    amount_entry = Entry(root)
    amount_entry.grid(row=1, column=1)

    Button(root, text="Deposit", command=handle_deposit).grid(row=2, column=0)
    Button(root, text="Withdraw", command=handle_withdraw).grid(row=2, column=1)
    Button(root, text="Check Balance", command=handle_check_balance).grid(row=3, column=0)
    Button(root, text="Predict Balance", command=handle_predict_balance).grid(row=3, column=1)

    root.mainloop()

gui()