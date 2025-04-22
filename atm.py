import sqlite3

class ATM:
    def __init__(self, account_number):
        self.conn = sqlite3.connect("atm.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.account_number = account_number

    def get_balance(self):
        self.cursor.execute("SELECT balance FROM users WHERE account_number=?", (self.account_number,))
        balance = self.cursor.fetchone()
        return balance[0] if balance else 0.0

    def deposit(self, amount):
        new_balance = self.get_balance() + amount
        self.cursor.execute("UPDATE users SET balance=? WHERE account_number=?", (new_balance, self.account_number))

        # Insert transaction record
        self.cursor.execute("INSERT INTO transactions (account_number, type, amount, balance_after) VALUES (?, 'Deposit', ?, ?)",
                            (self.account_number, amount, new_balance))

        self.conn.commit()
        return f"Deposited ₹{amount}. New Balance: ₹{new_balance:.2f}"

    def withdraw(self, amount):
        balance = self.get_balance()
        if amount > balance:
            return "Insufficient Balance!"
        
        new_balance = balance - amount
        self.cursor.execute("UPDATE users SET balance=? WHERE account_number=?", (new_balance, self.account_number))

        #  Insert transaction record
        self.cursor.execute("INSERT INTO transactions (account_number, type, amount, balance_after) VALUES (?, 'Withdraw', ?, ?)",
                            (self.account_number, amount, new_balance))

        self.conn.commit()
        return f"Withdrawn ₹{amount}. New Balance: ₹{new_balance:.2f}"

    def transfer(self, recipient_account, amount):
        balance = self.get_balance()
        if amount > balance:
            return "Insufficient Balance!"

        # Check if recipient exists
        self.cursor.execute("SELECT balance FROM users WHERE account_number=?", (recipient_account,))
        recipient = self.cursor.fetchone()
        if not recipient:
            return "Recipient account not found!"

        # Update sender balance
        new_sender_balance = balance - amount
        self.cursor.execute("UPDATE users SET balance=? WHERE account_number=?", (new_sender_balance, self.account_number))

        # Update recipient balance
        new_recipient_balance = recipient[0] + amount
        self.cursor.execute("UPDATE users SET balance=? WHERE account_number=?", (new_recipient_balance, recipient_account))

        #  Insert transaction records
        self.cursor.execute("INSERT INTO transactions (account_number, type, amount, balance_after) VALUES (?, 'Transfer Sent', ?, ?)",
                            (self.account_number, amount, new_sender_balance))
        self.cursor.execute("INSERT INTO transactions (account_number, type, amount, balance_after) VALUES (?, 'Transfer Received', ?, ?)",
                            (recipient_account, amount, new_recipient_balance))

        self.conn.commit()
        return f"Transferred ₹{amount} to {recipient_account}. New Balance: ₹{new_sender_balance:.2f}"

    def get_last_transactions(self, limit=5):
        self.cursor.execute("SELECT date, type, amount, balance_after FROM transactions WHERE account_number=? ORDER BY date DESC LIMIT ?",
                            (self.account_number, limit))
        transactions = self.cursor.fetchall()
        return [{"date": t[0], "type": t[1], "amount": t[2], "balance": t[3]} for t in transactions]

    def change_pin(self, new_pin):
        self.cursor.execute("UPDATE users SET pin=? WHERE account_number=?", (new_pin, self.account_number))
        self.conn.commit()
        return "PIN changed successfully!"

    def close(self):
        self.conn.close()
