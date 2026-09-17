from collections import defaultdict


class Analyzer:

    def __init__(self, db):
        self.db = db

    # --------------------------------
    # SUMMARY
    # --------------------------------

    def summary(self):

        rows = self.db.get_all()

        # Total credits
        credit = sum(
            row["amount"]
            for row in rows
            if row["type"] == "Credit"
        )

        # Total debits
        debit = sum(
            row["amount"]
            for row in rows
            if row["type"] == "Debit"
        )

        # Only debit amounts
        debits = [
            row["amount"]
            for row in rows
            if row["type"] == "Debit"
        ]

        categories = self.category_totals()

        return {
            "credit": credit,
            "debit": debit,
            "balance": credit - debit,
            "count": len(rows),
            "average_debit": (
                sum(debits) / len(debits)
                if debits
                else 0
            ),
            "top_category": (
                max(
                    categories,
                    key=categories.get
                )
                if categories
                else ""
            ),
            "unusual_count": len(
                self.unusual_transactions()
            )
        }

    # --------------------------------
    # CATEGORY TOTALS
    # --------------------------------

    def category_totals(self):

        totals = defaultdict(float)

        rows = self.db.get_all()

        for row in rows:

            if row["type"] == "Debit":

                totals[row["category"]] += (
                    row["amount"]
                )

        return dict(totals)

    # --------------------------------
    # AVERAGE DEBIT
    # --------------------------------

    def average_debit(self):

        rows = self.db.get_all()

        debits = [
            row["amount"]
            for row in rows
            if row["type"] == "Debit"
        ]

        if not debits:
            return 0

        return sum(debits) / len(debits)

    # --------------------------------
    # UNUSUAL TRANSACTIONS
    # --------------------------------

    def unusual_transactions(self):

        rows = self.db.get_all()

        average = self.average_debit()

        if average <= 0:
            return []

        unusual = [
            row
            for row in rows
            if (
                row["type"] == "Debit"
                and row["amount"] > average * 3
            )
        ]

        return unusual