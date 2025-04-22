import streamlit as st
import sqlite3
from atm import ATM

def signup():
    st.subheader("Create an Account")
    name = st.text_input("Full Name", key="signup_name")
    account_number = st.text_input("Account Number", key="signup_account")
    pin = st.text_input("Create PIN", type="password", key="signup_pin")

    if st.button("Sign Up"):
        conn = sqlite3.connect("atm.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (account_number, name, pin, balance) VALUES (?, ?, ?, ?)",
                           (account_number, name, pin, 0.0))
            conn.commit()
            st.success("Account Created Successfully! Please log in.")
        except sqlite3.IntegrityError:
            st.error("Account number already exists!")
        conn.close()

def login():
    st.subheader("Login to Your Account")
    account_number = st.text_input("Account Number", key="login_account")
    pin = st.text_input("Enter PIN", type="password", key="login_pin")

    if st.button("Login"):
        conn = sqlite3.connect("atm.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM users WHERE account_number=? AND pin=?", (account_number, pin))
        user = cursor.fetchone()
        conn.close()

        if user:
            st.session_state['logged_in'] = True
            st.session_state['account_number'] = account_number
            st.session_state['name'] = user[0]
            st.rerun()
        else:
            st.error("Invalid Account Number or PIN")


def logout():
    st.session_state.clear()
    st.rerun()

def atm_dashboard():
    st.sidebar.title("Customer Dashboard")
    atm = ATM(st.session_state['account_number'])
    st.sidebar.write(f"👤 **{st.session_state['name']}**")
    st.sidebar.write(f"🏦 **Account No: {st.session_state['account_number']}**")
    st.sidebar.write(f"💰 **Balance: ₹{atm.get_balance():.2f}**")

    choice = st.sidebar.radio("Choose an action", ["Deposit", "Withdraw", "Transfer", "Mini Statement"])

    if choice == "Deposit":
        amount = st.number_input("Enter amount to deposit", min_value=1)
        if st.button("Deposit"):
            st.success(atm.deposit(amount))

    elif choice == "Withdraw":
        amount = st.number_input("Enter amount to withdraw", min_value=1)
        if st.button("Withdraw"):
            st.success(atm.withdraw(amount))

    elif choice == "Transfer":
        receiver_acc = st.text_input("Recipient Account Number")
        amount = st.number_input("Enter amount", min_value=1)
        if st.button("Transfer"):
            st.success(atm.transfer(receiver_acc, amount))

    elif choice == "Mini Statement":
        transactions = atm.get_last_transactions()
        for txn in transactions:
            st.write(f"{txn['date']} | {txn['type']} | ₹{txn['amount']} | Balance: ₹{txn['balance']}")

    if st.button("Logout"):
        logout()

def main():
    st.title("💳 Virtual ATM System")

    if 'logged_in' not in st.session_state:
        login()
        st.markdown("---")
        signup()
    else:
        atm_dashboard()

if __name__ == "__main__":
    main()
