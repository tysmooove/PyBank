##############################################################################
# utils.py
# Shared input validation helpers used across all PyBank modules.
##############################################################################


# Functions
def get_valid_amount(prompt):
    """
    Prompt the user for a positive dollar amount.
    Loops until valid input is received.
    """
    while True:
        try:
            amount = float(input(prompt))
            if amount <= 0:
                print("  Amount must be greater than zero. Please try again.")
                continue
            return round(amount, 2)
        except ValueError:
            print("  Invalid input. Please enter a numeric amount.")


def get_valid_int(prompt, low, high):
    """
    Prompt the user for an integer between low and high (inclusive).
    Loops until valid input is received.
    """
    while True:
        try:
            value = int(input(prompt))
            if low <= value <= high:
                return value
            print(f"  Please enter a number between {low} and {high}.")
        except ValueError:
            print("  Invalid input. Please enter a whole number.")


def divider(char="=", width=50):
    """Print a divider line."""
    print(char * width)


def header(title):
    """Print a formatted section header."""
    divider()
    print(f"  {title}")
    divider()
