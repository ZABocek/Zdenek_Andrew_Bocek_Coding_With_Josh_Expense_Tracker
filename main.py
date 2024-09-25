from PyQt5.QtWidgets import (
    QApplication, QWidget, QTableWidgetItem, QMessageBox, QLabel, QLineEdit, QHeaderView, 
    QComboBox, QPushButton, QDateEdit, QTableWidget, QVBoxLayout, QHBoxLayout
)
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtCore import QDate, QRegularExpression, Qt
from PyQt5.QtGui import QRegularExpressionValidator, QFont
import sys
import re
import platform

class ExpenseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(600, 600)
        self.setWindowTitle("Expense Tracker 2.0")

        # Set Professional colors and background colors for different widgets
        self.setStyleSheet("""
            QWidget {
                background-color: #f7f7f7; /* Light gray background */
            }
            QLabel {
                color: #2e2e2e; /* Dark gray text */
                font-size: 10pt;
            }
            QLineEdit, QDateEdit {
                background-color: #ffffff; /* White background */
                color: #000000; /* Black text */
                border: 1px solid #cccccc; /* Light gray border */
                border-radius: 4px;
                padding: 4px;
            }
            QLineEdit:focus, QDateEdit:focus {
                border: 1px solid #5b9bd5; /* Soft blue border on focus */
            }
            QComboBox {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding-left: 4px;
                min-width: 80px; /* Ensure enough width */
            }
            QComboBox:focus {
                border: 1px solid #5b9bd5; /* Soft blue border on focus */
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #cccccc; /* Optional: Add a separator */
            }
            /* Removed QComboBox::down-arrow rule to use the default arrow */
            QTableWidget {
                background-color: #ffffff; /* White background */
                color: #000000; /* Black text */
                gridline-color: #dcdcdc; /* Light gray grid lines */
            }
            QHeaderView::section {
                background-color: #e2e2e2; /* Light gray header */
                color: #000000; /* Black text */
                padding: 4px;
                border: none;
                font-weight: bold;
            }
            QPushButton {
                background-color: #5b9bd5; /* Soft blue background */
                color: #ffffff; /* White text */
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #4a86c5; /* Slightly darker blue on hover */
            }
            QPushButton:pressed {
                background-color: #3c78b5; /* Even darker blue when pressed */
            }
        """)  

        # Determine the operating system
        system_platform = platform.system()

        # Set professional font for labels and inputs
        if system_platform == 'Windows':
            professional_font_name = "Segoe UI"
        elif system_platform == 'Darwin':  # Mac OS
            professional_font_name = "Helvetica Neue"
        else:
            professional_font_name = "Arial"  # As a fallback for Linux or others

        professional_font = QFont(professional_font_name, 10)

        # Set font for table contents
        self.table_font = QFont(professional_font_name, 10)

        # Currency data with symbols and formatting
        self.currency_data = {
            'USD': {'symbol': '$', 'decimal_sep': '.', 'thousand_sep': ','},
            'EUR': {'symbol': '€', 'decimal_sep': ',', 'thousand_sep': '.'},
            'GBP': {'symbol': '£', 'decimal_sep': '.', 'thousand_sep': ','},
            'JPY': {'symbol': '¥', 'decimal_sep': '.', 'thousand_sep': ','},
            'AUD': {'symbol': '$', 'decimal_sep': '.', 'thousand_sep': ','},
            'CAD': {'symbol': '$', 'decimal_sep': '.', 'thousand_sep': ','},
            'CHF': {'symbol': 'CHF', 'decimal_sep': '.', 'thousand_sep': '\''},
            'CNY': {'symbol': '¥', 'decimal_sep': '.', 'thousand_sep': ','},
            'SEK': {'symbol': 'kr', 'decimal_sep': ',', 'thousand_sep': ' '},
            'NZD': {'symbol': '$', 'decimal_sep': '.', 'thousand_sep': ','},
            'CZK': {'symbol': 'Kč', 'decimal_sep': ',', 'thousand_sep': ' '},
            'PLN': {'symbol': 'zł', 'decimal_sep': ',', 'thousand_sep': ' '},
            'HUF': {'symbol': 'Ft', 'decimal_sep': ',', 'thousand_sep': ' '},
            'DKK': {'symbol': 'kr', 'decimal_sep': ',', 'thousand_sep': '.'},
            'NOK': {'symbol': 'kr', 'decimal_sep': ',', 'thousand_sep': ' '},
            'RUB': {'symbol': '₽', 'decimal_sep': ',', 'thousand_sep': ' '},
            'TRY': {'symbol': '₺', 'decimal_sep': ',', 'thousand_sep': '.'},
            'ISK': {'symbol': 'kr', 'decimal_sep': '.', 'thousand_sep': ','},
            'RON': {'symbol': 'lei', 'decimal_sep': ',', 'thousand_sep': '.'},
            'HRK': {'symbol': 'kn', 'decimal_sep': ',', 'thousand_sep': '.'},
            'SKK': {'symbol': 'Sk', 'decimal_sep': ',', 'thousand_sep': ' '},  # Slovak Koruna (historic)
            # Add more currencies as needed
        }

        self.date_box = QDateEdit()
        self.date_box.setDate(QDate.currentDate())
        self.dropdown = QComboBox()
        self.amount = QLineEdit()
        self.description = QLineEdit()
        self.currency_dropdown = QComboBox()

        # Apply professional font to labels and inputs
        self.date_label = QLabel("Date:")
        self.date_label.setFont(professional_font)
        self.date_box.setFont(professional_font)

        self.category_label = QLabel("Category:")
        self.category_label.setFont(professional_font)
        self.dropdown.setFont(professional_font)

        self.amount_label = QLabel("Amount:")
        self.amount_label.setFont(professional_font)
        self.amount.setFont(professional_font)

        self.currency_label = QLabel("Currency:")
        self.currency_label.setFont(professional_font)
        self.currency_dropdown.setFont(professional_font)

        self.description_label = QLabel("Description:")
        self.description_label.setFont(professional_font)
        self.description.setFont(professional_font)

        self.add_button = QPushButton("Add Expense")
        self.insert_button = QPushButton("Insert Expense")
        self.delete_button = QPushButton("Delete Expense")
        self.add_button.clicked.connect(self.add_expense)
        self.insert_button.clicked.connect(self.insert_expense)
        self.delete_button.clicked.connect(self.delete_expense)

        # Apply professional font to buttons
        self.add_button.setFont(professional_font)
        self.insert_button.setFont(professional_font)
        self.delete_button.setFont(professional_font)

        # Populate currency dropdown with currencies
        self.currency_dropdown.addItems(sorted(self.currency_data.keys()))

        self.amount.textChanged.connect(self.format_amount)
        self.currency_dropdown.currentIndexChanged.connect(self.update_currency_formatting)

        # Placeholder for the validator, will be set in update_currency_formatting
        self.validator = None

        self.table = QTableWidget()
        self.table.setColumnCount(6)  # ID, date, category, amount, currency, description
        self.table.setHorizontalHeaderLabels(["Id", "Date", "Category", "Amount", "Currency", "Description"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setFont(self.table_font)  # Set professional font for table

        self.dropdown.addItems(sorted([
            "Rent", "Utilities", "House Payment", "Internet", "Savings (Acorn)", "Savings Account",
            "Medicaid", "GoodRX", "Medication Payment", "Medicare (Part B)", "Medicare (Part A)",
            "American Health Insurance", "Czech Health Insurance", "German Health Insurance",
            "Slovak Health Insurance", "American Dental Insurance", "Czech Dental Insurance",
            "German Dental Insurance", "Slovak Dental Insurance", "Teeth Cleaning", "Night Guard",
            "Dental Work", "Uber Ride", "Bus Ride", "Tram Ride", "Subway Ride", "Train Ride",
            "Train (Snack)", "Train (Drink)", "Taxi Ride", "Plane Ticket",
            "Plane (Select Seating)", "Plane (Upgrade Seat)", "Plane (Baggage Payment)",
            "Plane (Internet Payment)", "Plane (Buy Alcohol)", "Plane (Buy Snack)",
            "Food Delivery", "Takeout", "Dining Out", "Food", "Dessert", "Drinks", "Alcohol",
            "Marijuana", "Clothing", "Shoes", "Regular Book Purchase",
            "Regular Newspaper Purchase", "Furniture", "Mattress", "Painting", "Kitchen Appliance",
            "Computer", "Printer", "Electronics", "TV Payment", "Dishware/Tableware", "Cutlery",
            "Household Cleaning Supplies", "Miscellaneous Apartment Items", "Google One",
            "New York Times", "Der Spiegel", "Amazon Prime", "Amazon (Purchase Video)",
            "Amazon Kindle (Purchase Book)", "Amazon Kindle (Audio Book)", "YouTube Music Premium",
            "DVD", "CD", "Crunchyroll Subscription", "Crunchyroll Merchandise",
            "Czech Phone Payment", "German Phone Payment", "Google Phone Payment", "Netflix",
            "Disney+", "ChatGPT", "App Deploying Service", "Payment for AI", "Disney+ Package",
            "Hulu", "ESPN", "Adobe Scan", "Duolingo", "Tinder", "New York Times Cooking",
            "Adobe Acrobat Reader: Edit PDF"
        ]))

        # Layouts
        self.master_layout = QVBoxLayout()
        self.row1 = QHBoxLayout()
        self.row2a = QHBoxLayout()
        self.row2b = QHBoxLayout()
        self.row3 = QHBoxLayout()

        self.row1.addWidget(self.date_label)
        self.row1.addWidget(self.date_box)
        self.row1.addWidget(self.category_label)
        self.row1.addWidget(self.dropdown)

        self.row2a.addWidget(self.amount_label)
        self.row2a.addWidget(self.amount)
        self.row2a.addWidget(self.currency_label)
        self.row2a.addWidget(self.currency_dropdown)

        self.row2b.addWidget(self.description_label)
        self.row2b.addWidget(self.description)

        self.row3.addWidget(self.add_button)
        self.row3.addWidget(self.insert_button)
        self.row3.addWidget(self.delete_button)

        self.master_layout.addLayout(self.row1)
        self.master_layout.addLayout(self.row2a)
        self.master_layout.addLayout(self.row2b)
        self.master_layout.addLayout(self.row3)
        self.master_layout.addWidget(self.table)

        self.setLayout(self.master_layout)

        # Initialize currency formatting
        self.update_currency_formatting()

        self.load_table()

    def update_currency_formatting(self):
        currency = self.currency_dropdown.currentText()
        decimal_sep = self.currency_data[currency]['decimal_sep']
        thousand_sep = self.currency_data[currency]['thousand_sep']

        # Update the regular expression validator
        escaped_decimal_sep = re.escape(decimal_sep)
        escaped_thousand_sep = re.escape(thousand_sep)

        reg_ex_pattern = f"^-?[0-9{escaped_thousand_sep}]*{escaped_decimal_sep}?[0-9]*$"

        reg_ex = QRegularExpression(reg_ex_pattern)
        validator = QRegularExpressionValidator(reg_ex, self.amount)
        self.amount.setValidator(validator)

        # Update the amount field to reformat existing text if any
        self.format_amount()

    def format_amount(self):
        """Format the amount with commas/periods as user types, according to currency."""
        cursor_pos = self.amount.cursorPosition()
        text = self.amount.text()

        currency = self.currency_dropdown.currentText()
        decimal_sep = self.currency_data[currency]['decimal_sep']
        thousand_sep = self.currency_data[currency]['thousand_sep']

        # Remove thousand separators to work with the raw number
        text_without_thousand_sep = text.replace(thousand_sep, '')
        # Keep track of the position of the cursor in the text without thousand separators
        cursor_pos_without_thousand_sep = cursor_pos - text[:cursor_pos].count(thousand_sep)

        if text_without_thousand_sep:
            try:
                # Check for negative sign
                negative = False
                if text_without_thousand_sep.startswith('-'):
                    negative = True
                    text_without_thousand_sep = text_without_thousand_sep[1:]
                    cursor_pos_without_thousand_sep -= 1

                # Separate integer and decimal parts
                if decimal_sep in text_without_thousand_sep:
                    integer_part, decimal_part = text_without_thousand_sep.split(decimal_sep, 1)
                else:
                    integer_part = text_without_thousand_sep
                    decimal_part = ''

                # Remove any non-digit characters
                integer_part = re.sub(r'\D', '', integer_part)
                decimal_part = re.sub(r'\D', '', decimal_part)

                # Format the integer part with thousand separators
                if integer_part:
                    reversed_integer = integer_part[::-1]
                    grouped = [reversed_integer[i:i+3] for i in range(0, len(reversed_integer), 3)]
                    integer_part_with_thousand_sep = thousand_sep.join(grouped)[::-1]
                else:
                    integer_part_with_thousand_sep = ''

                # Reconstruct the formatted text
                if decimal_part != '':
                    formatted_text = integer_part_with_thousand_sep + decimal_sep + decimal_part
                else:
                    # Check if user typed a decimal separator at the end
                    if decimal_sep in text_without_thousand_sep and text_without_thousand_sep.endswith(decimal_sep):
                        formatted_text = integer_part_with_thousand_sep + decimal_sep
                    else:
                        formatted_text = integer_part_with_thousand_sep

                if negative:
                    formatted_text = '-' + formatted_text
                    cursor_pos_without_thousand_sep += 1

                # Update the cursor position based on the new formatted text
                new_cursor_pos = 0
                idx_without_thousand_sep = 0
                for idx_with_thousand_sep, char in enumerate(formatted_text):
                    if idx_without_thousand_sep >= cursor_pos_without_thousand_sep:
                        break
                    if char != thousand_sep:
                        idx_without_thousand_sep += 1
                    new_cursor_pos += 1

                self.amount.blockSignals(True)
                self.amount.setText(formatted_text)
                self.amount.setCursorPosition(new_cursor_pos)
                self.amount.blockSignals(False)
            except ValueError:
                # If input is not a valid number, do not format
                pass
        else:
            self.amount.blockSignals(True)
            self.amount.clear()
            self.amount.blockSignals(False)

    def load_table(self):
        self.table.setRowCount(0)

        query = QSqlQuery("SELECT * FROM expenses ORDER BY id DESC")
        row = 0
        while query.next():
            expense_id = query.value(0)
            date = query.value(1)
            category = query.value(2)
            amount = query.value(3)
            currency = query.value(4)
            description = query.value(5)

            self.table.insertRow(row)

            # Get the currency data
            currency_data = self.currency_data.get(currency, {'symbol': '', 'decimal_sep': '.', 'thousand_sep': ','})
            symbol = currency_data['symbol']
            decimal_sep = currency_data['decimal_sep']
            thousand_sep = currency_data['thousand_sep']

            # Format the amount
            amount_str = "{:,.2f}".format(amount)
            # Replace the decimal point and thousand separator as per currency
            amount_str = amount_str.replace(',', 'TEMP').replace('.', decimal_sep).replace('TEMP', thousand_sep)
            formatted_amount = f"{symbol}{amount_str}"

            # Create table items with professional font
            item_id = QTableWidgetItem(str(expense_id))
            item_date = QTableWidgetItem(date)
            item_category = QTableWidgetItem(category)
            item_amount = QTableWidgetItem(formatted_amount)
            item_currency = QTableWidgetItem(currency)
            item_description = QTableWidgetItem(description)

            # Set professional font to table items using self.table_font
            item_id.setFont(self.table_font)
            item_date.setFont(self.table_font)
            item_category.setFont(self.table_font)
            item_amount.setFont(self.table_font)
            item_currency.setFont(self.table_font)
            item_description.setFont(self.table_font)

            self.table.setItem(row, 0, item_id)
            self.table.setItem(row, 1, item_date)
            self.table.setItem(row, 2, item_category)
            self.table.setItem(row, 3, item_amount)
            self.table.setItem(row, 4, item_currency)
            self.table.setItem(row, 5, item_description)

            row += 1

    def add_expense(self):
        date = self.date_box.date().toString("dd-MM-yyyy")
        category = self.dropdown.currentText()
        amount_text = self.amount.text()
        description = self.description.text()
        currency = self.currency_dropdown.currentText()
        decimal_sep = self.currency_data[currency]['decimal_sep']
        thousand_sep = self.currency_data[currency]['thousand_sep']

        # Remove thousand separators
        amount_text = amount_text.replace(thousand_sep, '')
        # Replace decimal separator with '.'
        amount_text = amount_text.replace(decimal_sep, '.')

        try:
            amount = float(amount_text)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid amount.")
            return

        # Get the next available id using COALESCE to handle empty tables
        query = QSqlQuery("SELECT COALESCE(MAX(id), 0) FROM expenses")
        if query.next():
            max_id = int(query.value(0))
        else:
            max_id = 0

        new_id = max_id + 1

        insert_query = QSqlQuery()
        insert_query.prepare("INSERT INTO expenses (id, date, category, amount, currency, description) VALUES (?, ?, ?, ?, ?, ?)")
        insert_query.addBindValue(new_id)
        insert_query.addBindValue(date)
        insert_query.addBindValue(category)
        insert_query.addBindValue(amount)
        insert_query.addBindValue(currency)
        insert_query.addBindValue(description)
        if not insert_query.exec_():
            error = insert_query.lastError().text()
            QMessageBox.critical(self, "Database Error", error)
            print("Database Error in add_expense:", error)  # Optional: Print error to console
            return

        # Reset input fields
        self.date_box.setDate(QDate.currentDate())
        self.dropdown.setCurrentIndex(0)
        self.currency_dropdown.setCurrentIndex(0)
        self.amount.clear()
        self.description.clear()

        self.load_table()

    def insert_expense(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "No Row Selected", "Please select a row to insert the new expense after.")
            return

        # Get the selected row's ID
        selected_id = int(self.table.item(selected_row, 0).text())

        # Shift all the rows with id >= selected_id + 1
        shift_query = QSqlQuery()
        shift_query.prepare("UPDATE expenses SET id = id + 1 WHERE id >= ?")
        shift_query.addBindValue(selected_id + 1)
        if not shift_query.exec_():
            error = shift_query.lastError().text()
            QMessageBox.critical(self, "Database Error", error)
            print("Database Error in shift_query:", error)  # Optional: Print error to console
            return

        # Insert new expense at the next ID
        date = self.date_box.date().toString("dd-MM-yyyy")
        category = self.dropdown.currentText()
        amount_text = self.amount.text()
        description = self.description.text()
        currency = self.currency_dropdown.currentText()
        decimal_sep = self.currency_data[currency]['decimal_sep']
        thousand_sep = self.currency_data[currency]['thousand_sep']

        # Remove thousand separators
        amount_text = amount_text.replace(thousand_sep, '')
        # Replace decimal separator with '.'
        amount_text = amount_text.replace(decimal_sep, '.')

        try:
            amount = float(amount_text)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid amount.")
            return

        insert_query = QSqlQuery()
        insert_query.prepare("INSERT INTO expenses (id, date, category, amount, currency, description) VALUES (?, ?, ?, ?, ?, ?)")
        insert_query.addBindValue(selected_id + 1)
        insert_query.addBindValue(date)
        insert_query.addBindValue(category)
        insert_query.addBindValue(amount)
        insert_query.addBindValue(currency)
        insert_query.addBindValue(description)
        if not insert_query.exec_():
            error = insert_query.lastError().text()
            QMessageBox.critical(self, "Database Error", error)
            print("Database Error in insert_expense:", error)  # Optional: Print error to console
            return

        # Reset input fields
        self.date_box.setDate(QDate.currentDate())
        self.dropdown.setCurrentIndex(0)
        self.currency_dropdown.setCurrentIndex(0)
        self.amount.clear()
        self.description.clear()

        self.load_table()

    def delete_expense(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "No Expense Chosen", "Please choose an expense to delete.")
            return

        expense_id = int(self.table.item(selected_row, 0).text())

        confirm = QMessageBox.question(self, "Are you sure?", "Delete expense?", QMessageBox.Yes | QMessageBox.No)

        if confirm == QMessageBox.No:
            return

        query = QSqlQuery()
        query.prepare("DELETE FROM expenses WHERE id = ?")
        query.addBindValue(expense_id)
        if not query.exec_():
            error = query.lastError().text()
            QMessageBox.critical(self, "Database Error", error)
            print("Database Error in delete_expense:", error)  # Optional: Print error to console
            return

        # Reorder the remaining IDs after deletion
        reorder_query = QSqlQuery()
        reorder_query.prepare("UPDATE expenses SET id = id - 1 WHERE id > ?")
        reorder_query.addBindValue(expense_id)
        if not reorder_query.exec_():
            error = reorder_query.lastError().text()
            QMessageBox.critical(self, "Database Error", error)
            print("Database Error in reorder_query:", error)  # Optional: Print error to console
            return

        self.load_table()

# Initialize the database
database = QSqlDatabase.addDatabase("QSQLITE")
database.setDatabaseName("expense.db")
if not database.open():
    QMessageBox.critical(None, "Error", "Could not open your database")
    sys.exit(1)

# Adjust the table schema
query = QSqlQuery()
query.exec_("""CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY,
    date TEXT,
    category TEXT,
    amount REAL,
    currency TEXT,
    description TEXT
)""")

if __name__ == "__main__":
    app = QApplication([])
    main = ExpenseApp()
    main.show()
    app.exec_()
