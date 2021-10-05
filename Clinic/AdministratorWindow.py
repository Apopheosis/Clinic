from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *
from DatabaseHandler import fetch_doctors, fetch_patients, fetch_experts

class AW(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(QSize(480, 480))
        self.setWindowTitle("Администратор")

        center = QWidget(self)
        self.setCentralWidget(center)

        DocLabel = QLabel("Врачи:")
        ExpLabel = QLabel("Эксперты:")
        PatLabel = QLabel("Пациенты:")
        backBtn = QPushButton("Назад")

        grid_layout = QGridLayout()
        center.setLayout(grid_layout)

        Doctorstable = QTableWidget(self)
        Doctorstable.setColumnCount(4)
        doctors = fetch_doctors()
        row_count = len(doctors)
        Doctorstable.setRowCount(row_count)

        Doctorstable.setHorizontalHeaderLabels(["id", "Имя", "Фамилия", "Возраст"])
        for row in range(row_count):
            for col in range(4):
                Doctorstable.setItem(row, col, QTableWidgetItem(str(list(doctors[row].values())[col-4])))

        Doctorstable.resizeColumnsToContents()

        Expertstable = QTableWidget(self)
        Expertstable.setColumnCount(4)
        experts = fetch_experts()
        row_count = len(experts)
        Expertstable.setRowCount(row_count)

        Expertstable.setHorizontalHeaderLabels(["id", "Имя", "Фамилия", "Возраст"])
        for row in range(row_count):
            for col in range(4):
                Expertstable.setItem(row, col, QTableWidgetItem(str(list(experts[row].values())[col-4])))

        Expertstable.resizeColumnsToContents()

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
    
        grid_layout.addWidget(DocLabel, 0, 0)
        grid_layout.addWidget(Doctorstable)
        grid_layout.addWidget(ExpLabel)
        grid_layout.addWidget(Expertstable)
        grid_layout.addWidget(PatLabel)
        grid_layout.addWidget(Patientstable)
        grid_layout.addWidget(backBtn)

        backBtn.clicked.connect(self.ButtonBackPushed)

    def ButtonBackPushed(self):
        self.close()

        
        
        

        
