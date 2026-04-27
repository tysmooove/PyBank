##############################################################################
# account.py
# Handles bank account creation, retrieval, and interest calculation.
##############################################################################

# Imports
from database import get_connection


# Functions
def create_account(user_id, account_type):
    """Create a new account of the given type for the specified user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO accounts (user_id, account_type, balance) VALUES (?, ?, 0.0)",
        (user_id, account_type)
    )
    conn.commit()
    conn.close()


def get_accounts(user_id):
    """Return a list of all accounts belonging to the given user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM accounts WHERE user_id = ? ORDER BY created_at",
        (user_id,)
    )
    accounts = cursor.fetchall()
    conn.close()
    return [dict(a) for a in accounts]


def get_balance(account_id):
    """Return the current balance of the given account."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE id = ?", (account_id,))
    row = cursor.fetchone()
    conn.close()
    return row["balance"] if row else None


def apply_interest(account_id, rate=0.03):
    """
    Apply monthly interest at the given rate to a Savings account.
    Records the interest as a transaction.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT balance, account_type FROM accounts WHERE id = ?",
        (account_id,)
    )
    row = cursor.fetchone()
    if row and row["account_type"] == "Savings":
        interest = round(row["balance"] * rate, 2)
        if interest > 0:
            cursor.execute(
                "UPDATE accounts SET balance = balance + ? WHERE id = ?",
                (interest, account_id)
            )
            cursor.execute(
                """INSERT INTO transactions
                   (account_id, transaction_type, amount, description)
                   VALUES (?, 'interest', ?, 'Monthly Interest Applied')""",
                (account_id, interest)
            )
            conn.commit()
            conn.close()
            return interest
    conn.close()
    return 0


def display_accounts(accounts):
    """Print a formatted list of accounts."""
    if not accounts:
        print("  No accounts found.")
        return
    print(f"  {'#':<4} {'Type':<12} {'Balance':>12}")
    print("  " + "-" * 30)
    for i, acct in enumerate(accounts, 1):
        print(f"  {i:<4} {acct['account_type']:<12} ${acct['balance']:>11,.2f}")
