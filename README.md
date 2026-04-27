[README.md](https://github.com/user-attachments/files/27109182/README.md)
# PyBank 🏦
### Personal Banking Management System

A lightweight, offline, privacy-first personal banking simulator built entirely in Python. No internet required. No sign-ups. No paywalls. Just run it and go.

---

## What is PyBank?

PyBank is a command-line Python application that simulates a real personal banking system. Users can register and log in securely, create multiple bank accounts, move money around, and view a complete history of every transaction — all stored locally in a SQLite database file on your own machine.

Built as a capstone project for CIS4930 — Python Application Development at Florida State University.

---

## Features

| Feature | Description |
|---|---|
| 🔐 Secure Login | SHA-256 password hashing on registration and login |
| 🏦 Account Management | Create Checking and Savings accounts per user |
| 💵 Deposit & Withdraw | Live balance updates with full input validation |
| 🔄 Fund Transfers | Atomic transfers between your own accounts |
| 📋 Transaction History | Full log of every transaction with timestamps |
| 📄 Account Statements | Formatted statement display + CSV file export |
| 📈 Interest Calculation | 3% monthly interest applied to Savings accounts |
| 🗄️ SQLite Storage | All data stored locally — no cloud, no sharing |

---

## Requirements

- Python 3.x
- No external libraries needed — uses only Python built-ins:
  - `sqlite3` — database storage
  - `hashlib` — password hashing
  - `csv` — statement export
  - `getpass` — hidden password input

---

## How to Run

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/pybank.git
cd pybank
```

**2. Run the program**
```bash
python main.py
```

**3. That's it.** A `pybank.db` file is created automatically on first run. All your data is saved there.

---

## File Structure

```
pybank/
│
├── main.py          # Entry point — all menu navigation and user interaction
├── database.py      # SQLite connection and table initialization
├── auth.py          # User registration and login with SHA-256 hashing
├── account.py       # Account creation, balance retrieval, interest logic
├── transaction.py   # Deposit, withdraw, transfer, and history functions
├── reports.py       # Statement display and CSV export
├── utils.py         # Shared input validation helpers
└── pybank.db        # SQLite database (auto-created on first run)
```

---

## Demo

```
==================================================
  WELCOME TO PYBANK
  Personal Banking Management System
==================================================
  1. Register
  2. Login
  3. Exit
==================================================
  Select an option: 2

==================================================
  LOGIN
==================================================
  Username: tyler
  Password:

  Login successful. Welcome back, tyler!

==================================================
  PYBANK  |  TYLER
==================================================
  1. View Accounts
  2. Create Account
  3. Deposit
  4. Withdraw
  5. Transfer
  6. Transaction History
  7. Account Statement
  8. Apply Interest (Savings)
  9. Logout
==================================================
```

---

## Security Note

Passwords are never stored in plain text. Every password is hashed using SHA-256 via Python's built-in `hashlib` module before being written to the database. The program also uses `getpass` so your password is never visible while you type it in the terminal.

---

## Resetting the Database

If you want to start fresh, just delete the `pybank.db` file and run the program again. A brand new empty database will be created automatically.

```bash
rm pybank.db
python main.py
```

---

## Future Improvements

- Tkinter GUI to replace the command-line interface
- Login attempt limiter to lock accounts after failed tries
- Monthly spending summary and budget categories
- Full database encryption at rest
- Web interface using Flask or Django

---

## Course Info

**Course:** CIS4930 — Python Application Development
**Student:** Tyler Hawkins
**Term:** Spring 2026
**Institution:** Florida State University

---

## License

This project was built for educational purposes as part of a course capstone assignment.
