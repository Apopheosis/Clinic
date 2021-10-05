from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *
from DatabaseHandler import get_questions, Database_connect, send_questions, delete_question

class EW(QMainWindow):
    def __init__(self, questions):

        super().__init__()

        self.setMinimumSize(QSize(480, 480))
        self.setWindowTitle("Эксперт")

        self.Exp = None

        buttonSyn = QPushButton("Синхронизировать с базой")
        buttonNew = QPushButton("Новый вопрос")
        buttonDel = QPushButton("Удалить вопрос")
        buttonBack = QPushButton("Назад")

        center = QWidget(self)
        self.setCentralWidget(center)

        grid_layout = QGridLayout()
        center.setLayout(grid_layout)

        self.Questionstable = QTableWidget(self)
        self.Questionstable.setColumnCount(3)
        PrSt = Database_connect()
        create_questions_table_query = """CREATE TABLE IF NOT EXISTS questions (
            qid INT AUTO_INCREMENT PRIMARY KEY,
            question TEXT,
            right_answer VARCHAR(45)
        );
        """
        PrSt.cursor().execute(create_questions_table_query)

        self.row_count = len(questions)

        self.Questionstable.setHorizontalHeaderLabels(["qid", "Вопрос", "Ответ"])

        if self.row_count > 0:
            self.Questionstable.setRowCount(self.row_count+1)

            for row in range(self.row_count):
                for col in range(3):
                    self.Questionstable.setItem(row, col, QTableWidgetItem(str(list(questions[row].values())[col-3])))
        else:
            self.row_count += 1
            self.Questionstable.setRowCount(self.row_count)

            for col in range(3):
                self.Questionstable.setItem(1, col, QTableWidgetItem(str(list((1, " ", " ")))))
        self.Questionstable.resizeColumnsToContents()

        grid_layout.addWidget(self.Questionstable)
        grid_layout.addWidget(buttonSyn)
        grid_layout.addWidget(buttonNew)
        grid_layout.addWidget(buttonDel)
        grid_layout.addWidget(buttonBack)

        

        buttonSyn.clicked.connect(self.ButtonSynPushed)
        buttonBack.clicked.connect(self.Back)
        buttonNew.clicked.connect(self.addRow)
        buttonDel.clicked.connect(self.delRow)

    def ButtonSynPushed(self):
        for row in range(self.Questionstable.rowCount()):
            quest = []
            for col in range(3):
                if self.Questionstable.item(row, col) is not None:
                    quest.append(self.Questionstable.item(row, col).text())
            if len(quest) == 3:
                send_questions(quest)
                self.Exp = EW(get_questions("questions"))
                self.Exp.show()
                self.close()
            else:
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Ошибка")
                dlg.setText("Недостаточно данных!")
                dlg.exec()                    

        
    def addRow(self):
        row_count = self.Questionstable.rowCount()
        self.Questionstable.insertRow(row_count)
        self.Questionstable.setItem(row_count, 0, QTableWidgetItem(str(row_count+1)))

    def delRow(self):
        curRow = self.Questionstable.currentRow()
        delete_question(self.Questionstable.item(curRow, 0))
        self.Questionstable.removeRow(curRow)

    def Back(self):
        self.close()
                
                
            
        
