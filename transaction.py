##############################################################################
# transaction.py
# Handles all money movement: deposits, withdrawals, transfers, and history.
##############################################################################

# Imports
from database import get_connection


# Functions
def deposit(account_id, amount):
    """
    Deposit amount into the given account.
    Records the transaction and updates the balance.
    Returns True on success.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE accounts SET balance = balance + ? WHERE id = ?",
        (amount, account_id)
    )
    cursor.execute(
        """INSERT INTO transactions
           (account_id, transaction_type, amount, description)
           VALUES (?, 'deposit', ?, 'Deposit')""",
        (account_id, amount)
    )
    conn.commit()
    conn.close()
    return True


def withdraw(account_id, amount):
    """
    Withdraw amount from the given account if funds are sufficient.
    Returns True on success, False if insufficient funds.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE id = ?", (account_id,))
    row = cursor.fetchone()

    if not row or row["balance"] < amount:
        conn.close()
        return False

    cursor.execute(
        "UPDATE accounts SET balance = balance - ? WHERE id = ?",
        (amount, account_id)
    )
    cursor.execute(
        """INSERT INTO transactions
           (account_id, transaction_type, amount, description)
           VALUES (?, 'withdrawal', ?, 'Withdrawal')""",
        (account_id, amount)
    )
    conn.commit()
    conn.close()
    return True


def transfer(from_id, to_id, amount):
    """
    Transfer amount from one account to another atomically.
    Returns True on success, False if insufficient funds.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE id = ?", (from_id,))
    row = cursor.fetchone()

    if not row or row["balance"] < amount:
        conn.close()
        return False

    try:
        cursor.execute(
            "UPDATE accounts SET balance = balance - ? WHERE id = ?",
            (amount, from_id)
        )
        cursor.execute(
            "UPDATE accounts SET balance = balance + ? WHERE id = ?",
            (amount, to_id)
        )
        cursor.execute(
            """INSERT INTO transactions
               (account_id, transaction_type, amount, description)
               VALUES (?, 'transfer_out', ?, 'Transfer Out')""",
            (from_id, amount)
        )
        cursor.execute(
            """INSERT INTO transactions
               (account_id, transaction_type, amount, description)
               VALUES (?, 'transfer_in', ?, 'Transfer In')""",
            (to_id, amount)
        )
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        return False
    finally:
        conn.close()


def get_transaction_history(account_id):
    """Return all transactions for the given account, newest first."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT * FROM transactions
           WHERE account_id = ?
           ORDER BY timestamp DESC""",
        (account_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def display_history(transactions):
    """Print a formatted transaction history table."""
    if not transactions:
        print("  No transactions found.")
        return
    print(f"  {'Date & Time':<22} {'Type':<15} {'Amount':>10}")
    print("  " + "-" * 50)
    for t in transactions:
        ttype = t["transaction_type"].replace("_", " ").title()
        ts    = t["timestamp"][:16]
        print(f"  {ts:<22} {ttype:<15} ${t['amount']:>9,.2f}")
