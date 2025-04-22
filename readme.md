# Virtual ATM Machine

This project is a simple virtual ATM built using Python, Streamlit for the UI, and SQLite for the database. It allows users to create an account, log in, check balance, deposit money, withdraw money, and log out.

## Features

- Signup and Login with PIN
- Deposit and Withdraw Money
- Check Account Balance
- Logout Option
- Uses SQLite to store user data
- Python OOP used to structure the backend logic

## Files in the Project

- `app.py` - Main file with Streamlit interface
- `atm_module.py` - Python class that handles ATM operations
- `database.py` - Sets up the SQLite database and creates tables
- `atm.db` - The SQLite database file (auto-generated)
- `README.md` - Project information

## How to Run

1. Make sure Python is installed (Python 3.7 or later).
2. Install Streamlit if not already installed:

```bash
pip install streamlit
Run the app from the terminal:

bash
streamlit run app.py
The app will open in your browser.

Database Table
The app uses one table called users with these fields:

account_number (text, unique ID)

name (text)

pin (text)

balance (real number)

Notes
This project is for learning purposes only.

In real applications, PINs should be encrypted.

Author
Om Nanaware
Ketki gaikwad
Prachee Wakode
