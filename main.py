##############################################################################
# main.py
# PyBank — Personal Banking Management System
# Entry point. Handles all menu navigation and user interaction.
##############################################################################

# Imports
from database import initialize_db
from auth import register_user, login_user
from account import (create_account, get_accounts,
                     display_accounts, apply_interest)
from transaction import (deposit, withdraw, transfer,
                         get_transaction_history, display_history)
from reports import print_statement, export_statement
from utils import get_valid_amount, get_valid_int, divider, header


# Function Declarations
def pick_account(user_id, prompt="Select an account: "):
    """
    Display the user's accounts and return the selected account dict.
    Returns None if the user has no accounts.
    """
    accounts = get_accounts(user_id)
    if not accounts:
        print("\n  You have no accounts yet. Please create one first.")
        return None
    print()
    display_accounts(accounts)
    choice = get_valid_int(f"\n  {prompt}", 1, len(accounts))
    return accounts[choice - 1]


def handle_register():
    """Walk the user through creating a new PyBank account."""
    header("REGISTER")
    username = input("  Choose a username: ").strip()
    if not username:
        print("  Username cannot be blank.")
        return
    password = input("  Choose a password: ").strip()
    if not password:
        print("  Password cannot be blank.")
        return

    if register_user(username, password):
        print(f"\n  Account created successfully! Welcome, {username}.")
    else:
        print("\n  That username is already taken. Please try another.")


def handle_login():
    """Verify credentials and open the banking menu on success."""
    header("LOGIN")
    username = input("  Username: ").strip()
    password = input("  Password: ").strip()
    user = login_user(username, password)

    if user:
        print(f"\n  Login successful. Welcome back, {username}!")
        banking_menu(user)
    else:
        print("\n  Invalid username or password. Please try again.")


def handle_create_account(user_id):
    """Let the user create a Checking or Savings account."""
    header("CREATE ACCOUNT")
    print("  1. Checking")
    print("  2. Savings")
    choice = get_valid_int("\n  Select account type: ", 1, 2)
    acct_type = "Checking" if choice == 1 else "Savings"
    create_account(user_id, acct_type)
    print(f"\n  {acct_type} account created successfully!")


def handle_deposit(user_id):
    """Deposit funds into a selected account."""
    header("DEPOSIT")
    acct = pick_account(user_id, "Select account to deposit into: ")
    if not acct:
        return
    amount = get_valid_amount("\n  Enter deposit amount: $")
    deposit(acct["id"], amount)
    print(f"\n  Successfully deposited ${amount:,.2f}.")
    print(f"  New balance: ${acct['balance'] + amount:,.2f}")


def handle_withdraw(user_id):
    """Withdraw funds from a selected account."""
    header("WITHDRAW")
    acct = pick_account(user_id, "Select account to withdraw from: ")
    if not acct:
        return
    amount = get_valid_amount("\n  Enter withdrawal amount: $")
    success = withdraw(acct["id"], amount)
    if success:
        print(f"\n  Successfully withdrew ${amount:,.2f}.")
        print(f"  New balance: ${acct['balance'] - amount:,.2f}")
    else:
        print("\n  Insufficient funds. Transaction cancelled.")


def handle_transfer(user_id):
    """Transfer funds between two of the user's accounts."""
    header("TRANSFER")
    accounts = get_accounts(user_id)
    if len(accounts) < 2:
        print("\n  You need at least two accounts to make a transfer.")
        return

    print("\n  --- Transfer FROM ---")
    display_accounts(accounts)
    from_choice = get_valid_int("\n  Select source account: ", 1, len(accounts))
    from_acct   = accounts[from_choice - 1]

    print("\n  --- Transfer TO ---")
    display_accounts(accounts)
    to_choice = get_valid_int("\n  Select destination account: ", 1, len(accounts))
    to_acct   = accounts[to_choice - 1]

    if from_acct["id"] == to_acct["id"]:
        print("\n  Source and destination cannot be the same account.")
        return

    amount  = get_valid_amount("\n  Enter transfer amount: $")
    success = transfer(from_acct["id"], to_acct["id"], amount)

    if success:
        print(f"\n  Successfully transferred ${amount:,.2f}")
        print(f"  From: {from_acct['account_type']}  -->  To: {to_acct['account_type']}")
    else:
        print("\n  Insufficient funds. Transfer cancelled.")


def handle_history(user_id):
    """Display transaction history for a selected account."""
    header("TRANSACTION HISTORY")
    acct = pick_account(user_id, "Select account to view history: ")
    if not acct:
        return
    history = get_transaction_history(acct["id"])
    print(f"\n  --- {acct['account_type']} Account History ---")
    display_history(history)


def handle_statement(user_id):
    """Display and optionally export an account statement."""
    header("ACCOUNT STATEMENT")
    acct = pick_account(user_id, "Select account: ")
    if not acct:
        return
    print_statement(acct["id"], acct["account_type"])

    export = input("\n  Export to CSV? (y/n): ").strip().lower()
    if export == "y":
        filename = export_statement(acct["id"], acct["account_type"])
        print(f"  Statement exported to: {filename}")


def handle_interest(user_id):
    """Apply monthly interest to a Savings account."""
    header("APPLY INTEREST")
    accounts = [a for a in get_accounts(user_id) if a["account_type"] == "Savings"]
    if not accounts:
        print("\n  You have no Savings accounts.")
        return
    print()
    display_accounts(accounts)
    choice   = get_valid_int("\n  Select Savings account: ", 1, len(accounts))
    acct     = accounts[choice - 1]
    interest = apply_interest(acct["id"])
    if interest > 0:
        print(f"\n  Interest of ${interest:,.2f} applied at 3% monthly rate.")
    else:
        print("\n  No interest applied (balance may be zero).")


def banking_menu(user):
    """Main banking menu shown after a successful login."""
    while True:
        print()
        divider()
        print(f"  PYBANK  |  {user['username'].upper()}")
        divider()
        print("  1. View Accounts")
        print("  2. Create Account")
        print("  3. Deposit")
        print("  4. Withdraw")
        print("  5. Transfer")
        print("  6. Transaction History")
        print("  7. Account Statement")
        print("  8. Apply Interest (Savings)")
        print("  9. Logout")
        divider()

        choice = input("  Select an option: ").strip()

        if choice == "1":
            header("YOUR ACCOUNTS")
            accounts = get_accounts(user["id"])
            display_accounts(accounts)
        elif choice == "2":
            handle_create_account(user["id"])
        elif choice == "3":
            handle_deposit(user["id"])
        elif choice == "4":
            handle_withdraw(user["id"])
        elif choice == "5":
            handle_transfer(user["id"])
        elif choice == "6":
            handle_history(user["id"])
        elif choice == "7":
            handle_statement(user["id"])
        elif choice == "8":
            handle_interest(user["id"])
        elif choice == "9":
            print(f"\n  Logged out. Goodbye, {user['username']}!")
            break
        else:
            print("\n  Invalid option. Please enter a number from 1 to 9.")


def main_menu():
    """Application entry point and main menu loop."""
    initialize_db()

    while True:
        print()
        divider()
        print("  WELCOME TO PYBANK")
        print("  Personal Banking Management System")
        divider()
        print("  1. Register")
        print("  2. Login")
        print("  3. Exit")
        divider()

        choice = input("  Select an option: ").strip()

        if choice == "1":
            handle_register()
        elif choice == "2":
            handle_login()
        elif choice == "3":
            print("\n  Thank you for using PyBank. Goodbye!")
            break
        else:
            print("\n  Invalid option. Please enter 1, 2, or 3.")


# Entry Point
if __name__ == "__main__":
    main_menu()
