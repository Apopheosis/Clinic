from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *
from DatabaseHandler import fetch_patients


class PT(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Пациенты")
        self.setFixedSize(QSize(400, 400))

        Patientstable = QTableWidget(self)
        Patientstable.setColumnCount(5)
        patients = fetch_patients()
        row_count = len(patients)
        Patientstable.setRowCount(row_count)

        Patientstable.setHorizontalHeaderLabels(["id", "Имя", "Фамилия", "Возраст", "Диагноз"])
        for row in range(row_count):
            for col in range(5):
                Patientstable.setItem(row, col, QTableWidgetItem(str(list(patients[row].values())[col-5])))

        Patientstable.resizeColumnsToContents()

        
        self.setCentralWidget(Patientstable)
