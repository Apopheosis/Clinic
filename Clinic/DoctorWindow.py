from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *
from DatabaseHandler import fetch_patients, get_questions, Database_connect, create_question_list
from DiagnosisWindow import DIA
from PatientTable import PT

class DW(QMainWindow):

    def __init__(self):
        
        super().__init__()

        self.setWindowTitle("Врач")
        self.setMinimumSize(QSize(480, 480))

        pageLayout = QVBoxLayout()

        diagLayout = QHBoxLayout()
        QuestionListLayout = QHBoxLayout()
        QuestionsLayout = QHBoxLayout()
        btnLayout = QHBoxLayout()
        labelLayout = QHBoxLayout()

        self.DIA = None
        self.Table = None

        self.QuestionListtable = QTableWidget()
        self.QuestionListtable.setColumnCount(4)
        self.QuestionListtable.setEditTriggers(QTableWidget.NoEditTriggers)

        self.Questionstable = QTableWidget()
        self.Questionstable.setColumnCount(3)
        self.Questionstable.setEditTriggers(QTableWidget.NoEditTriggers)

        QuestionListLabel = QLabel("Вопросная карточка пациента:")
        QuestionsLabel = QLabel("Вопросы экспертов:")

        DiagBtn = QPushButton("Диагноз")
        SendBtn = QPushButton("Отправить пациенту")
        PatientsBtn = QPushButton("Пациенты")
        AddBtn = QPushButton("↑")
        RemoveBtn = QPushButton("↓")
        self.PatientsBox = QComboBox()
        
        patients = fetch_patients()
        for patient in patients:
            self.PatientsBox.addItem(str(patient['idpatients']))
        print(patients)

        self.QuestionListtable.setHorizontalHeaderLabels(["qid", "Вопрос", "Ответ", "Правильный ответ"])
        self.Questionstable.setHorizontalHeaderLabels(["qid", "Вопрос", "Ответ"])

        questions = get_questions("questions")

        self.Questionstable.setRowCount(len(questions))
        for row in range(len(questions)):
            for col in range(3):
                self.Questionstable.setItem(row, col, QTableWidgetItem(str(list(questions[row].values())[col-3])))
        idpatient = self.PatientsBox.currentText()
        create_question_list(idpatient)
        self.patientQuestList = get_questions("patient_"+str(idpatient))

        self.QuestionListtable.setRowCount(len(self.patientQuestList))
        
        for row in range(len(self.patientQuestList)):
            for col in range(4):
                self.QuestionListtable.setItem(row, col, QTableWidgetItem(str(list(self.patientQuestList[row].values())[col-4])))                


        diagLayout.addWidget(QuestionListLabel)
        diagLayout.addWidget(SendBtn)
        diagLayout.addWidget(PatientsBtn)
        diagLayout.addWidget(DiagBtn)
        QuestionListLayout.addWidget(self.QuestionListtable)
        btnLayout.addWidget(AddBtn)
        btnLayout.addWidget(self.PatientsBox)
        btnLayout.addWidget(RemoveBtn)
        labelLayout.addWidget(QuestionsLabel)
        QuestionsLayout.addWidget(self.Questionstable)
        
        pageLayout.addLayout(diagLayout)
        pageLayout.addLayout(QuestionListLayout)
        pageLayout.addLayout(btnLayout)
        pageLayout.addLayout(labelLayout)
        pageLayout.addLayout(QuestionsLayout)

        container = QWidget()
        container.setLayout(pageLayout)
        self.setCentralWidget(container)

        AddBtn.clicked.connect(self.AddToQuestList)
        RemoveBtn.clicked.connect(self.RemoveFromQuestList)
        self.PatientsBox.currentTextChanged.connect(self.changePatient)
        SendBtn.clicked.connect(self.SendToDatabase)
        DiagBtn.clicked.connect(self.openDiagWindow)
        PatientsBtn.clicked.connect(self.openPatientsTable)

    def SendToDatabase(self):
        idpatient = self.PatientsBox.currentText()
        PrSt = Database_connect()
        with PrSt.cursor() as cursor:
            for row in range(self.QuestionListtable.rowCount()):
               query_arguments = []
               for col in range(4):
                   if self.QuestionListtable.item(row, col) is None:
                       query_arguments.append(" ")
                   else:    
                       query_arguments.append(self.QuestionListtable.item(row, col).text())   
               cursor.execute("INSERT INTO patient_" + idpatient + " (qid, question, right_answer) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE qid=%s, question=%s, right_answer=%s",
                            (query_arguments[0], query_arguments[1], query_arguments[3], query_arguments[0], query_arguments[1], query_arguments[3]))
        PrSt.commit()
        

    def changePatient(self):
        idpatient = self.PatientsBox.currentText()
        patientQuestList = get_questions("patient_" + str(idpatient))

        self.QuestionListtable.clearContents()
        

        self.QuestionListtable.setRowCount(len(patientQuestList))

        for row in range(len(patientQuestList)):
            for col in range(4):
                self.QuestionListtable.setItem(row, col, QTableWidgetItem(str(list(self.patientQuestList[row].values())[col-4])))
            

    def RemoveFromQuestList(self):
        curRow = self.QuestionListtable.currentRow()
        self.QuestionListtable.removeRow(curRow)

    def AddToQuestList(self):
        curRow = self.Questionstable.currentRow()
        self.QuestionListtable.insertRow(self.QuestionListtable.rowCount())
        self.QuestionListtable.setItem(self.QuestionListtable.rowCount()-1,
                                       0,
                                       QTableWidgetItem(self.Questionstable.item(curRow, 0)))
        self.QuestionListtable.setItem(self.QuestionListtable.rowCount()-1,
                                       1,
                                       QTableWidgetItem(self.Questionstable.item(curRow, 1)))
        self.QuestionListtable.setItem(self.QuestionListtable.rowCount()-1,
                                       3,
                                       QTableWidgetItem(self.Questionstable.item(curRow, 2)))

    def openDiagWindow(self):
        self.DIA = DIA(self.PatientsBox.currentText(), self.QuestionListtable)
        self.DIA.show()
        
    def openPatientsTable(self):
        self.Table = PT()
        self.Table.show()
            
        
        
