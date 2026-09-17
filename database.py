import csv
from pathlib import Path


# Project folder
BASE_DIR = Path(__file__).resolve().parent

# CSV file location
DATA_FILE = BASE_DIR / "data" / "transactions.csv"


class TransactionDB:

    def __init__(self):

        # Location of CSV database
        self.path = DATA_FILE

        # Create data folder if it doesn't exist
        self.path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        # CSV columns
        self.fields = [
            "id",
            "date",
            "type",
            "category",
            "amount",
            "mode",
            "description"
        ]

        # Create empty CSV if it doesn't exist
        if not self.path.exists():
            self.create_file()

    # --------------------------------
    # CREATE EMPTY DATABASE
    # --------------------------------

    def create_file(self):

        with self.path.open(
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow(self.fields)

    # --------------------------------
    # GET ALL TRANSACTIONS
    # --------------------------------

    def get_all(self):

        if not self.path.exists():
            self.create_file()

        with self.path.open(
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            rows = list(
                csv.DictReader(file)
            )

        # Convert amount from string to number
        for row in rows:
            row["amount"] = float(
                row["amount"]
            )

        return rows

    # --------------------------------
    # ADD TRANSACTION
    # --------------------------------

    def add(self, data):

        rows = self.get_all()

        # Find existing transaction numbers
        numbers = []

        for row in rows:

            try:
                number = int(
                    str(row["id"]).replace(
                        "TX", ""
                    )
                )

                numbers.append(number)

            except (ValueError, TypeError):
                pass

        # Generate next ID
        next_number = max(
            numbers,
            default=0
        ) + 1

        row = {
            "id": f"TX{next_number:03d}",
            "date": data["date"],
            "type": data["type"],
            "category": data["category"],
            "amount": data["amount"],
            "mode": data["mode"],
            "description": data["description"]
        }

        # Save transaction
        with self.path.open(
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=self.fields
            )

            writer.writerow(row)

        return row

    # --------------------------------
    # CLEAR ALL TRANSACTIONS
    # --------------------------------

    def clear(self):

        # Empty the database.
        # No demo data is added.

        self.create_file()