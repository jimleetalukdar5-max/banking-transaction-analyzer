VALID_TYPES = {
    "Debit",
    "Credit"
}

VALID_CATEGORIES = {
    "Food",
    "Shopping",
    "Travel",
    "Salary",
    "Bills",
    "Other"
}

VALID_MODES = {
    "UPI",
    "Card",
    "NEFT",
    "IMPS",
    "Cash"
}


def validate_transaction(data):

    # Check transaction type
    if data["type"] not in VALID_TYPES:
        raise ValueError("Transaction type is invalid.")

    # Check category
    if data["category"] not in VALID_CATEGORIES:
        raise ValueError("Category is invalid.")

    # Check payment mode
    if data["mode"] not in VALID_MODES:
        raise ValueError("Payment mode is invalid.")

    # Check amount
    amount = data["amount"]

    if amount <= 0:
        raise ValueError("Amount must be greater than ₹0.")

    if amount > 10_000_000:
        raise ValueError("Amount is above the allowed limit.")

    # Check description
    if not data["description"]:
        raise ValueError("Description cannot be empty.")

    if len(data["description"]) > 100:
        raise ValueError(
            "Description must be 100 characters or less."
        )

    # Check date
    if not data.get("date"):
        raise ValueError("Date is required.")

    return True