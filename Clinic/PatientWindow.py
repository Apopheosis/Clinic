from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *
from DatabaseHandler import send_answer

class PW(QWidget):
    def __init__(self, index, question, pid):
        super().__init__()

        self.question = question
        self.pid = pid
        self.maxim = len(self.question)
        self.index = index
        self.Pat = None
        print(self.maxim)


        self.setWindowTitle("Вопрос №" + str(question[self.index]['qid']))
        self.setFixedSize(QSize(300, 400))


        questionLayout = QHBoxLayout()
        answerLayout = QHBoxLayout()
        pageLayout = QVBoxLayout()

        self.questionLabel = QLabel(question[self.index]['question'])
        self.questionLabel.setAlignment(Qt.AlignCenter)
        buttonYes = QPushButton("Да")
        buttonNo = QPushButton("Нет")

        questionLayout.addWidget(self.questionLabel)
        answerLayout.addWidget(buttonYes)
        answerLayout.addWidget(buttonNo)

        pageLayout.addLayout(questionLayout)
        pageLayout.addLayout(answerLayout)

        self.setLayout(pageLayout)

        buttonYes.clicked.connect(self.ButtonYesAction)
        buttonNo.clicked.connect(self.ButtonNoAction)
        
    def ButtonYesAction(self):
        table = "patient_" + str(self.pid)
        send_answer(self.question[self.index]['qid'], 'Да', table)
        if (self.index<self.maxim-1):
            self.Pat = PW(self.index + 1, self.question, self.pid)
            self.Pat.show()
        self.close()
        
    def ButtonNoAction(self):
        table = "patient_" + str(self.pid)
        send_answer(self.question[self.index]['qid'], 'Нет', table)
        if (self.index<self.maxim-1):
            self.Pat = PW(self.index + 1, self.question, self.pid)
            self.Pat.show()
        self.close()
        

        
