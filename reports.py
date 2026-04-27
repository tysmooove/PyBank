##############################################################################
# reports.py
# Handles account statement display and CSV export.
##############################################################################

# Imports
import csv
from transaction import get_transaction_history
from account import get_balance


# Functions
def print_statement(account_id, account_type):
    """Print a formatted account statement to the console."""
    balance = get_balance(account_id)
    history = get_transaction_history(account_id)

    print()
    print("=" * 50)
    print(f"  ACCOUNT STATEMENT — {account_type.upper()}")
    print("=" * 50)
    print(f"  Current Balance: ${balance:,.2f}")
    print("-" * 50)

    if not history:
        print("  No transactions on record.")
    else:
        print(f"  {'Date & Time':<22} {'Type':<15} {'Amount':>10}")
        print("  " + "-" * 48)
        for t in history:
            ttype = t["transaction_type"].replace("_", " ").title()
            ts    = t["timestamp"][:16]
            print(f"  {ts:<22} {ttype:<15} ${t['amount']:>9,.2f}")

    print("=" * 50)


def export_statement(account_id, account_type):
    """
    Export the account statement to a CSV file.
    Returns the filename on success.
    """
    filename = f"statement_account_{account_id}.csv"
    history  = get_transaction_history(account_id)
    balance  = get_balance(account_id)

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["PyBank Account Statement"])
        writer.writerow(["Account Type", account_type])
        writer.writerow(["Current Balance", f"${balance:,.2f}"])
        writer.writerow([])
        writer.writerow(["Date & Time", "Type", "Amount", "Description"])
        for t in history:
            writer.writerow([
                t["timestamp"][:16],
                t["transaction_type"].replace("_", " ").title(),
                f"${t['amount']:,.2f}",
                t["description"]
            ])

    return filename
