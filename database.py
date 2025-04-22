import sqlite3

def init_db():
    conn = sqlite3.connect("atm.db")
    cursor = conn.cursor()

    #  Users Table (Holds account details)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            account_number TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            pin TEXT NOT NULL,
            balance REAL DEFAULT 0.0,
            email TEXT,
            phone TEXT
        )
    """)

    #  Transactions Table (Stores transaction history)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_number TEXT,
            type TEXT,  -- Deposit, Withdraw, Transfer
            amount REAL,
            balance_after REAL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(account_number) REFERENCES users(account_number)
        )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
