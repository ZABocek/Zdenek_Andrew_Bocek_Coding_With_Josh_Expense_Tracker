from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem, QMessageBox, QLabel, QLineEdit, QComboBox, QPushButton, QDateEdit, QTableWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtCore import QDate
import sys
import re

class ExpenseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(550, 500)
        self.setWindowTitle("Expense Tracker 2.0")
        
        self.date_box = QDateEdit()
        self.dropdown = QComboBox()
        self.amount = QLineEdit()
        self.description = QLineEdit()
        
        self.add_button = QPushButton("Add Expense")
        self.insert_button = QPushButton("Insert Expense")
        self.delete_button = QPushButton("Delete Expense")
        self.add_button.clicked.connect(self.add_expense)
        self.insert_button.clicked.connect(self.insert_expense)
        self.delete_button.clicked.connect(self.delete_expense)
        
        self.amount.textChanged.connect(self.format_amount)  # Connect the signal to the custom slot
        
        self.table = QTableWidget()
        self.table.setColumnCount(5) # ID, date, category, amount, description
        self.table.setHorizontalHeaderLabels(["Id", "Date", "Category", "Amount", "Description"])
        
        self.dropdown.addItems(sorted(["Rent", "Utilities", "House Payment", "Internet", "Savings (Acorn)", "Savings Account", 
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
                                       "Adobe Acrobat Reader: Edit PDF"]))
        
        self.master_layout = QVBoxLayout()
        self.row1 = QHBoxLayout()
        self.row2 = QHBoxLayout()
        self.row3 = QHBoxLayout()
        
        self.row1.addWidget(QLabel("Date:"))
        self.row1.addWidget(self.date_box)
        self.row1.addWidget(QLabel("Category:"))
        self.row1.addWidget(self.dropdown)
        
        self.row2.addWidget(QLabel("Amount:"))
        self.row2.addWidget(self.amount)
        self.row2.addWidget(QLabel("Description:"))
        self.row2.addWidget(self.description)
        
        self.row3.addWidget(self.add_button)
        self.row3.addWidget(self.insert_button)
        self.row3.addWidget(self.delete_button)
        
        self.master_layout.addLayout(self.row1)
        self.master_layout.addLayout(self.row2)
        self.master_layout.addLayout(self.row3)
        
        self.master_layout.addWidget(self.table)
        
        self.setLayout(self.master_layout)
        
        self.load_table()

    def format_amount(self):
        """Format the amount with commas as user types."""
        cursor_pos = self.amount.cursorPosition()
        text = self.amount.text()
        # Remove commas to work with the raw number
        text_without_commas = text.replace(",", "")
        # Keep track of the position of the cursor in the text without commas
        cursor_pos_without_commas = cursor_pos - text[:cursor_pos].count(',')

        if text_without_commas:
            # Ensure that the input is numeric
            try:
                # Check for negative sign
                negative = False
                if text_without_commas.startswith('-'):
                    negative = True
                    text_without_commas = text_without_commas[1:]
                    cursor_pos_without_commas -= 1

                # Separate integer and decimal parts
                if '.' in text_without_commas:
                    integer_part, decimal_part = text_without_commas.split('.', 1)  # Use maxsplit=1
                else:
                    integer_part = text_without_commas
                    decimal_part = ''

                # Format the integer part with commas
                if integer_part:
                    integer_part_with_commas = "{:,}".format(int(integer_part))
                else:
                    integer_part_with_commas = ''

                # Reconstruct the formatted text
                if decimal_part != '':
                    formatted_text = integer_part_with_commas + '.' + decimal_part
                else:
                    # Check if user typed a decimal point at the end
                    if '.' in text_without_commas and text_without_commas.endswith('.'):
                        formatted_text = integer_part_with_commas + '.'
                    else:
                        formatted_text = integer_part_with_commas

                if negative:
                    formatted_text = '-' + formatted_text
                    cursor_pos_without_commas += 1

                # Update the cursor position based on the new formatted text
                new_cursor_pos = 0
                idx_without_commas = 0
                for idx_with_commas, char in enumerate(formatted_text):
                    if idx_without_commas >= cursor_pos_without_commas:
                        break
                    if char != ',':
                        idx_without_commas += 1
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
        
        query = QSqlQuery("SELECT * FROM expenses ORDER BY id ASC")
        row = 0
        while query.next():
            expense_id = query.value(0)
            date = query.value(1)
            category = query.value(2)
            amount = query.value(3)
            description = query.value(4)
            
            self.table.insertRow(row)
            
            self.table.setItem(row, 0, QTableWidgetItem(str(expense_id)))
            self.table.setItem(row, 1, QTableWidgetItem(date))
            self.table.setItem(row, 2, QTableWidgetItem(category))
            self.table.setItem(row, 3, QTableWidgetItem(str(amount)))
            self.table.setItem(row, 4, QTableWidgetItem(description))

            row += 1
            
    def add_expense(self):
        date = self.date_box.date().toString("dd-MM-yyyy")
        category = self.dropdown.currentText()
        amount_text = self.amount.text().replace(",", "")  # Remove commas before storing the value
        description = self.description.text()

        try:
            amount = float(amount_text)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid amount.")
            return
        
        query = QSqlQuery()
        query.prepare("""
                      INSERT INTO expenses (date, category, amount, description)
                      VALUES (?, ?, ?, ?)
                      """)
        query.addBindValue(date)
        query.addBindValue(category)
        query.addBindValue(amount)
        query.addBindValue(description)
        query.exec_()
        
        self.date_box.setDate(QDate.currentDate())
        self.dropdown.setCurrentIndex(0)
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
        
        # Shift all the rows below and including the selected row
        shift_query = QSqlQuery()
        shift_query.prepare("UPDATE expenses SET id = id + 1 WHERE id > ?")
        shift_query.addBindValue(selected_id)
        shift_query.exec_()

        # Insert new expense at the next ID
        date = self.date_box.date().toString("dd-MM-yyyy")
        category = self.dropdown.currentText()
        amount_text = self.amount.text().replace(",", "")  # Remove commas before storing the value
        description = self.description.text()

        try:
            amount = float(amount_text)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid amount.")
            return
        
        insert_query = QSqlQuery()
        insert_query.prepare("""
                             INSERT INTO expenses (id, date, category, amount, description)
                             VALUES (?, ?, ?, ?, ?)
                             """)
        insert_query.addBindValue(selected_id + 1)
        insert_query.addBindValue(date)
        insert_query.addBindValue(category)
        insert_query.addBindValue(amount)
        insert_query.addBindValue(description)
        insert_query.exec_()

        self.date_box.setDate(QDate.currentDate())
        self.dropdown.setCurrentIndex(0)
        self.amount.clear()
        self.description.clear()
        
        self.load_table()
        
    def delete_expense(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "No Expense Chosen", "Please choose an expense to delete.")
            return
        
        expense_id = int(self.table.item(selected_row,0).text())
        
        confirm = QMessageBox.question(self, "Are you sure?", "Delete expense?", QMessageBox.Yes | QMessageBox.No)
        
        if confirm == QMessageBox.No:
            return
        query = QSqlQuery()
        query.prepare("DELETE FROM expenses WHERE id = ?")
        query.addBindValue(expense_id)
        query.exec_()
        
        # Reorder the remaining IDs after deletion
        reorder_query = QSqlQuery("UPDATE expenses SET id = id - 1 WHERE id > ?")
        reorder_query.addBindValue(expense_id)
        reorder_query.exec_()
        
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
               description TEXT)""")
        
if __name__ == "__main__":
    app = QApplication([])
    main = ExpenseApp()
    main.show()
    app.exec_()
