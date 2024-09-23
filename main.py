from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem, QMessageBox, QLabel, QLineEdit, QComboBox, QPushButton, QDateEdit, QTableWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtCore import QDate
import sys

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
        self.delete_button = QPushButton("Delete Expense")
        self.add_button.clicked.connect(self.add_expense)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5) # ID, date, category, amount, description
        self.table.setHorizontalHeaderLabels(["Id", "Date", "Category", "Amount", "Description"])
        
        self.dropdown.addItems(["Rent", "Utilities", "House Payment", "Internet", "Savings (Acorn)", "Savings Account", 
                                "Medicaid", "GoodRX", "Medication Payment", "Medicare (Part B)", "Medicare (Part A)", 
                                "American Health Insurance", "Czech Health Insurance", "German Health Insurance", 
                                "Slovak Health Insurance", "Uber Ride", "Bus Ride", "Tram Ride", "Subway Ride", 
                                "Train Ride", "Train (Snack)", "Train (Drink)", "Taxi Ride", "Plane Ticket", 
                                "Plane (Select Seating)", "Plane (Upgrade Seat)", "Plane (Baggage Payment)", 
                                "Plane (Internet Payment)", "Plane (Buy Alcohol)", "Plane (Buy Snack)", 
                                "Food Delivery", "Takeout", "Dining Out", "Food", "Dessert", "Drinks", "Alcohol", 
                                "Marijuana", "Furniture", "Mattress", "Painting", "Kitchen Appliance", "Computer", 
                                "Printer", "Electronics", "TV Payment", "Dishware/Tableware", "Cutlery", 
                                "Miscellaneous Apartment Items", "Google One", "New York Times", "Der Spiegel", 
                                "Amazon Prime", "Czech Phone Payment", "German Phone Payment", "Google Phone Payment", 
                                "Netflix", "Disney+", "ChatGPT", "App Deploying Service", "Payment for AI", 
                                "Disney+ Package", "Hulu", "ESPN", "Adobe Scan", "Duolingo", "Tinder", 
                                "New York Times Cooking", "Adobe Acrobat Reader: Edit PDF"])
        
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
        self.row3.addWidget(self.delete_button)
        
        self.master_layout.addLayout(self.row1)
        self.master_layout.addLayout(self.row2)
        self.master_layout.addLayout(self.row3)
        
        self.master_layout.addWidget(self.table)
        
        self.setLayout(self.master_layout)
        
        self.load_table()
        
    def load_table(self):
        self.table.setRowCount(0)
        
        query = QSqlQuery("SELECT * FROM expenses")
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
        amount = self.amount.text()
        description = self.description.text()
        
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
        
database = QSqlDatabase.addDatabase("QSQLITE")
database.setDatabaseName("expense.db")
if not database.open():
    QMessageBox.critical(None, "Error", "Could not open your database")
    sys.exit(1)
    
query = QSqlQuery()
query.exec_("""
           CREATE TABLE IF NOT EXISTS expenses (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               date TEXT,
               category TEXT,
               amount REAL,
               description TEXT
           )
            """)
        
if __name__ in "__main__":
    app = QApplication([])
    main = ExpenseApp()
    main.show()
    app.exec_()