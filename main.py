import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from database import TransactionDB
from transaction import validate_transaction
from analyzer import Analyzer


class BankingTransactionAnalyzer:

    def __init__(self, root):

        self.root = root
        self.root.title("Banking Transaction Analyzer")
        self.root.geometry("1100x700")
        self.root.minsize(950, 600)

        self.db = TransactionDB()
        self.analyzer = Analyzer(self.db)

        self.setup_style()

        self.create_header()
        self.create_sidebar()
        self.create_main_area()

        self.show_dashboard()

    # ==========================================
    # STYLE
    # ==========================================

    def setup_style(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Treeview",
            rowheight=32,
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold")
        )

    # ==========================================
    # HEADER
    # ==========================================

    def create_header(self):

        header = tk.Frame(
            self.root,
            bg="#1f4e79",
            height=70
        )

        header.pack(
            side="top",
            fill="x"
        )

        title = tk.Label(
            header,
            text="Banking Transaction Analyzer",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#1f4e79"
        )

        title.pack(
            side="left",
            padx=25,
            pady=18
        )

    # ==========================================
    # SIDEBAR
    # ==========================================

    def create_sidebar(self):

        self.sidebar = tk.Frame(
            self.root,
            bg="#eeeeee",
            width=210
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        buttons = [
            ("Dashboard", self.show_dashboard),
            ("Add Transaction", self.show_add),
            ("Transactions", self.show_transactions),
            ("Spending Analysis", self.show_analysis),
            ("Clear All Data", self.clear_data)
        ]

        for text, command in buttons:

            button = tk.Button(
                self.sidebar,
                text=text,
                command=command,
                font=("Arial", 11),
                bg="#eeeeee",
                relief="flat",
                anchor="w",
                padx=20,
                pady=12,
                cursor="hand2"
            )

            button.pack(
                fill="x",
                padx=10,
                pady=4
            )

    # ==========================================
    # MAIN AREA
    # ==========================================

    def create_main_area(self):

        self.main_area = tk.Frame(
            self.root,
            bg="white"
        )

        self.main_area.pack(
            side="right",
            fill="both",
            expand=True
        )

    # ==========================================
    # CLEAR MAIN AREA
    # ==========================================

    def clear_main(self):

        for widget in self.main_area.winfo_children():
            widget.destroy()

    # ==========================================
    # SECTION TITLE
    # ==========================================

    def section_title(self, title):

        label = tk.Label(
            self.main_area,
            text=title,
            font=("Arial", 20, "bold"),
            bg="white",
            fg="#1f1f1f"
        )

        label.pack(
            anchor="w",
            padx=30,
            pady=(25, 15)
        )

    # ==========================================
    # CARD
    # ==========================================

    def card(self, parent, title, value):

        frame = tk.Frame(
            parent,
            bg="#f5f5f5",
            bd=1,
            relief="solid"
        )

        frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=8
        )

        tk.Label(
            frame,
            text=title,
            font=("Arial", 11),
            bg="#f5f5f5"
        ).pack(
            pady=(15, 5)
        )

        tk.Label(
            frame,
            text=value,
            font=("Arial", 18, "bold"),
            bg="#f5f5f5",
            fg="#1f4e79"
        ).pack(
            pady=(5, 15)
        )

    # ==========================================
    # DASHBOARD
    # ==========================================

    def show_dashboard(self):

        self.clear_main()

        self.section_title("Dashboard")

        summary = self.analyzer.summary()

        cards = tk.Frame(
            self.main_area,
            bg="white"
        )

        cards.pack(
            fill="x",
            padx=20
        )

        self.card(
            cards,
            "Total Credit",
            self.money(summary["credit"])
        )

        self.card(
            cards,
            "Total Debit",
            self.money(summary["debit"])
        )

        self.card(
            cards,
            "Balance",
            self.money(summary["balance"])
        )

        self.card(
            cards,
            "Transactions",
            str(summary["count"])
        )

        # --------------------------------------
        # RECENT TRANSACTIONS
        # --------------------------------------

        tk.Label(
            self.main_area,
            text="Recent Transactions",
            font=("Arial", 15, "bold"),
            bg="white"
        ).pack(
            anchor="w",
            padx=30,
            pady=(30, 10)
        )

        rows = self.db.get_all()

        if not rows:

            tk.Label(
                self.main_area,
                text="No transactions available.\n"
                     "Add a transaction to get started.",
                font=("Arial", 12),
                bg="white",
                fg="gray"
            ).pack(
                pady=50
            )

            return

        tree = self.make_tree(
            self.main_area
        )

        recent_rows = list(
            reversed(rows[-7:])
        )

        for row in recent_rows:
            self.insert_tree(
                tree,
                row
            )

    # ==========================================
    # ADD TRANSACTION
    # ==========================================

    def show_add(self):

        self.clear_main()

        self.section_title(
            "Add Transaction"
        )

        form = tk.Frame(
            self.main_area,
            bg="white"
        )

        form.pack(
            padx=50,
            pady=10,
            anchor="nw"
        )

        # --------------------------------------
        # TYPE
        # --------------------------------------

        tk.Label(
            form,
            text="Transaction Type",
            font=("Arial", 11),
            bg="white"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=8
        )

        self.type_var = tk.StringVar(
            value="Debit"
        )

        ttk.Combobox(
            form,
            textvariable=self.type_var,
            values=[
                "Debit",
                "Credit"
            ],
            state="readonly",
            width=30
        ).grid(
            row=0,
            column=1,
            padx=20,
            pady=8
        )

        # --------------------------------------
        # CATEGORY
        # --------------------------------------

        tk.Label(
            form,
            text="Category",
            font=("Arial", 11),
            bg="white"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=8
        )

        self.category_var = tk.StringVar(
            value="Food"
        )

        ttk.Combobox(
            form,
            textvariable=self.category_var,
            values=[
                "Food",
                "Shopping",
                "Travel",
                "Salary",
                "Bills",
                "Other"
            ],
            state="readonly",
            width=30
        ).grid(
            row=1,
            column=1,
            padx=20,
            pady=8
        )

        # --------------------------------------
        # AMOUNT
        # --------------------------------------

        tk.Label(
            form,
            text="Amount",
            font=("Arial", 11),
            bg="white"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=8
        )

        self.amount_entry = tk.Entry(
            form,
            width=33
        )

        self.amount_entry.grid(
            row=2,
            column=1,
            padx=20,
            pady=8
        )

        # --------------------------------------
        # PAYMENT MODE
        # --------------------------------------

        tk.Label(
            form,
            text="Payment Mode",
            font=("Arial", 11),
            bg="white"
        ).grid(
            row=3,
            column=0,
            sticky="w",
            pady=8
        )

        self.mode_var = tk.StringVar(
            value="UPI"
        )

        ttk.Combobox(
            form,
            textvariable=self.mode_var,
            values=[
                "UPI",
                "Card",
                "NEFT",
                "IMPS",
                "Cash"
            ],
            state="readonly",
            width=30
        ).grid(
            row=3,
            column=1,
            padx=20,
            pady=8
        )

        # --------------------------------------
        # DESCRIPTION
        # --------------------------------------

        tk.Label(
            form,
            text="Description",
            font=("Arial", 11),
            bg="white"
        ).grid(
            row=4,
            column=0,
            sticky="w",
            pady=8
        )

        self.description_entry = tk.Entry(
            form,
            width=33
        )

        self.description_entry.grid(
            row=4,
            column=1,
            padx=20,
            pady=8
        )

        # --------------------------------------
        # SAVE BUTTON
        # --------------------------------------

        tk.Button(
            form,
            text="Save Transaction",
            command=self.save_transaction,
            bg="#1f4e79",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=8,
            cursor="hand2"
        ).grid(
            row=5,
            column=1,
            sticky="w",
            padx=20,
            pady=20
        )

    # ==========================================
    # SAVE TRANSACTION
    # ==========================================

    def save_transaction(self):

        amount_text = self.amount_entry.get().strip()

        if not amount_text:

            messagebox.showerror(
                "Error",
                "Please enter an amount."
            )

            return

        try:

            amount = float(
                amount_text
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Amount must be a valid number."
            )

            return

        data = {
            "date": str(date.today()),
            "type": self.type_var.get(),
            "category": self.category_var.get(),
            "amount": amount,
            "mode": self.mode_var.get(),
            "description": (
                self.description_entry
                .get()
                .strip()
            )
        }

        try:

            validate_transaction(data)

            self.db.add(data)

            messagebox.showinfo(
                "Success",
                "Transaction added successfully."
            )

            self.show_dashboard()

        except ValueError as error:

            messagebox.showerror(
                "Invalid Transaction",
                str(error)
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"Could not save transaction:\n{error}"
            )

    # ==========================================
    # TRANSACTIONS
    # ==========================================

    def show_transactions(self):

        self.clear_main()

        self.section_title(
            "Transactions"
        )

        search_frame = tk.Frame(
            self.main_area,
            bg="white"
        )

        search_frame.pack(
            fill="x",
            padx=30,
            pady=5
        )

        tk.Label(
            search_frame,
            text="Search:",
            font=("Arial", 11),
            bg="white"
        ).pack(
            side="left"
        )

        search_entry = tk.Entry(
            search_frame,
            width=35
        )

        search_entry.pack(
            side="left",
            padx=10
        )

        tree = self.make_tree(
            self.main_area
        )

        rows = self.db.get_all()

        def search():

            query = (
                search_entry
                .get()
                .strip()
                .lower()
            )

            for item in tree.get_children():
                tree.delete(item)

            for row in rows:

                searchable = " ".join([
                    str(row["id"]),
                    str(row["date"]),
                    str(row["type"]),
                    str(row["category"]),
                    str(row["mode"]),
                    str(row["description"])
                ]).lower()

                if query in searchable:

                    self.insert_tree(
                        tree,
                        row
                    )

        tk.Button(
            search_frame,
            text="Search",
            command=search,
            bg="#1f4e79",
            fg="white",
            padx=15,
            cursor="hand2"
        ).pack(
            side="left"
        )

        for row in reversed(rows):

            self.insert_tree(
                tree,
                row
            )

    # ==========================================
    # SPENDING ANALYSIS
    # ==========================================

    def show_analysis(self):

        self.clear_main()

        self.section_title(
            "Spending Analysis"
        )

        summary = self.analyzer.summary()

        frame = tk.Frame(
            self.main_area,
            bg="white"
        )

        frame.pack(
            fill="x",
            padx=30
        )

        self.card(
            frame,
            "Average Debit",
            self.money(
                summary["average_debit"]
            )
        )

        self.card(
            frame,
            "Top Category",
            summary["top_category"]
            if summary["top_category"]
            else "N/A"
        )

        self.card(
            frame,
            "Unusual Transactions",
            str(summary["unusual_count"])
        )

        # --------------------------------------
        # CATEGORY BREAKDOWN
        # --------------------------------------

        tk.Label(
            self.main_area,
            text="Category-wise Spending",
            font=("Arial", 15, "bold"),
            bg="white"
        ).pack(
            anchor="w",
            padx=30,
            pady=(30, 10)
        )

        categories = (
            self.analyzer
            .category_totals()
        )

        if not categories:

            tk.Label(
                self.main_area,
                text="No debit transactions available.",
                font=("Arial", 12),
                bg="white",
                fg="gray"
            ).pack(
                pady=30
            )

            return

        tree = ttk.Treeview(
            self.main_area,
            columns=[
                "category",
                "amount"
            ],
            show="headings"
        )

        tree.heading(
            "category",
            text="Category"
        )

        tree.heading(
            "amount",
            text="Amount"
        )

        tree.column(
            "category",
            width=250
        )

        tree.column(
            "amount",
            width=200
        )

        tree.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=10
        )

        for category, amount in categories.items():

            tree.insert(
                "",
                "end",
                values=(
                    category,
                    self.money(amount)
                )
            )

    # ==========================================
    # TREEVIEW
    # ==========================================

    def make_tree(self, parent):

        columns = [
            "id",
            "date",
            "type",
            "category",
            "amount",
            "mode",
            "description"
        ]

        tree = ttk.Treeview(
            parent,
            columns=columns,
            show="headings"
        )

        headings = {
            "id": "ID",
            "date": "Date",
            "type": "Type",
            "category": "Category",
            "amount": "Amount",
            "mode": "Mode",
            "description": "Description"
        }

        widths = {
            "id": 80,
            "date": 100,
            "type": 80,
            "category": 100,
            "amount": 100,
            "mode": 90,
            "description": 250
        }

        for column in columns:

            tree.heading(
                column,
                text=headings[column]
            )

            tree.column(
                column,
                width=widths[column]
            )

        tree.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=10
        )

        return tree

    # ==========================================
    # INSERT TREE ROW
    # ==========================================

    def insert_tree(self, tree, row):

        tree.insert(
            "",
            "end",
            values=(
                row["id"],
                row["date"],
                row["type"],
                row["category"],
                self.money(row["amount"]),
                row["mode"],
                row["description"]
            )
        )

    # ==========================================
    # MONEY FORMAT
    # ==========================================

    def money(self, amount):

        return f"₹{amount:,.2f}"

    # ==========================================
    # CLEAR ALL DATA
    # ==========================================

    def clear_data(self):

        rows = self.db.get_all()

        if not rows:

            messagebox.showinfo(
                "No Data",
                "There are no transactions to clear."
            )

            return

        confirm = messagebox.askyesno(
            "Clear All Data",
            "Are you sure you want to delete "
            "all transactions?"
        )

        if confirm:

            self.db.clear()

            messagebox.showinfo(
                "Success",
                "All transaction data has been cleared."
            )

            self.show_dashboard()


# ==========================================
# START APPLICATION
# ==========================================

if __name__ == "__main__":

    root = tk.Tk()

    app = BankingTransactionAnalyzer(root)

    root.mainloop()