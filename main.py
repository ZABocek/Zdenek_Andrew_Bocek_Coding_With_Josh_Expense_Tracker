from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QDateEdit, QTableWidget, QVBoxLayout, QHBoxLayout

class ExpenseApp(QWidget):
    def __init__(self):
        self.resize(550, 500)
        self.setWindowTitle("Expense Tracker 2.0")
        
        self.date_box = QDateEdit()
        self.dropdown = QComboBox()
        self.amount = QLineEdit()
        self.description = QLineEdit()
        
        self.master_layout = QVBoxLayout()
        self.row1 = QHBoxLayout()
        self.row2 = QHBoxLayout()
        self.row3 = QHBoxLayout()
        
        self.add_button = QPushButton("Add Expense")
        self.delete_button = QPushButton("Delete Expense")
        
        self.table = QTableWidget()
        self.table.setColumnCount(5) # ID, date, category, amount, description
        self.table.setHorizontalHeaderLabels(["ID", "Date", "Category", "Amount", "Description"])
        