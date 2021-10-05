from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *
from DatabaseHandler import Database_connect

class DIA(QMainWindow):
    def __init__(self, idpat, table):

        super().__init__()

        self.setWindowTitle("Диагноз")

        progress = QProgressBar()
        self.idpat = idpat
        self.diagnosis = QLineEdit()
        diagBtn = QPushButton("Вынести диагноз")
        diagLayout = QHBoxLayout()
        PrSt = Database_connect()
        pageLayout = QVBoxLayout()
        with PrSt.cursor() as cursor:
            cursor.execute("SELECT name, lastname, age FROM patients WHERE idpatients=%s", (self.idpat))
            result = cursor.fetchone()

        PatientLabel = QLabel(result['name'] + " " + result['lastname'] + ", " + str(result['age']))
        progressLabel = QLabel("Процент здоровости: ")
        progress.setMinimum(0)
        progress.setMaximum(100)
        progress.reset()

        right = 0

        for row in range(table.rowCount()):
            if (table.item(row, 2) is not None) and (table.item(row, 3) is not None):
                if table.item(row, 2).text()==table.item(row,3).text():
                    right += 1

        rightPercent = (right/table.rowCount())*100

        progress.setValue(rightPercent)

        diagLayout.addWidget(self.diagnosis)
        diagLayout.addWidget(diagBtn)

        pageLayout.addWidget(PatientLabel)
        pageLayout.addWidget(progressLabel)
        pageLayout.addWidget(progress)
        pageLayout.addLayout(diagLayout)
        

        container = QWidget()
        container.setLayout(pageLayout)
        self.setCentralWidget(container)

        diagBtn.clicked.connect(self.setDiagnosis)

    def setDiagnosis(self):
        PrSt = Database_connect()
        with PrSt.cursor() as cursor:
            cursor.execute("UPDATE patients SET diagnosis=%s WHERE idpatients=%s", (self.diagnosis.text(), self.idpat))
        PrSt.commit()

        
        

        
