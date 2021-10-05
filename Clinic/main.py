from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *
import pymysql
from RegWindow import RW
from PatientWindow import PW
from AdministratorWindow import AW
from ExpertWindow import EW
from DoctorWindow import DW
from config import host, port, user, password, db_name
from DatabaseHandler import fetch_user, get_questions, create_question_list,get_patient_id


import sys



class MainWindow(QMainWindow):
    

    def __init__(self):
        super().__init__()

        self.Reg = None
        self.Pat = None
        self.Adm = None
        self.Exp = None
        self.Doc = None

        self.setWindowTitle("Клиника")


        self.loginInput = QLineEdit()
        self.passwordInput = QLineEdit()
        self.passwordInput.setEchoMode(QLineEdit.Password)
        loginLabel = QLabel("Логин:")
        passwordLabel = QLabel("Пароль:")

        
        buttonEnter = QPushButton("Вход")
        buttonReg = QPushButton("Регистрация")
        self.setFixedSize(QSize(300, 400))

        pageLayout = QVBoxLayout()
        loginLayout = QHBoxLayout()
        passwordLayout = QHBoxLayout()
        buttonLayout = QHBoxLayout()

        loginLayout.addWidget(loginLabel)
        loginLayout.addWidget(self.loginInput)
        passwordLayout.addWidget(passwordLabel)
        passwordLayout.addWidget(self.passwordInput)
        buttonLayout.addWidget(buttonEnter)
        buttonLayout.addWidget(buttonReg)

        pageLayout.addLayout(loginLayout)
        pageLayout.addLayout(passwordLayout)
        pageLayout.addLayout(buttonLayout)

        container = QWidget()
        container.setLayout(pageLayout)
        
        self.setCentralWidget(container)

        buttonEnter.clicked.connect(self.ButtonEnterPushed)
        buttonReg.clicked.connect(self.ButtonRegPushed)
    



    def ButtonEnterPushed(self):
        if (self.loginInput.text()=='')or(self.passwordInput.text()==''):
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Поля пусты!")
            dlg.setText("Заполните поля логина и/или пароля!")
            dlg.exec()
        else:
            res = fetch_user(self.loginInput.text(), self.passwordInput.text())
            if res is not None:
                if res['occupation']=="Пациент":
                    idpat = get_patient_id(res['name'],res['lastname'],res['age'])
                    create_question_list(idpat)
                    table = "patient_" + str(idpat) 
                    questions = get_questions(table)
                    if len(questions)>0:
                        
                        self.Pat = PW(0, questions, idpat)
                        self.Pat.show()
                    else:
                        dlg = QMessageBox(self)
                        dlg.setWindowTitle("Подождите!")
                        dlg.setText("Вопросов для вас пока что нет.")
                        dlg.exec()
                elif res['occupation']=="Врач":
                    self.Doc = DW()
                    self.Doc.show()
                elif res['occupation']=="Администратор":
                    self.Adm = AW()
                    self.Adm.show()
                elif res['occupation']=="Эксперт":
                    self.Exp = EW(get_questions("questions"))
                    self.Exp.show()
            else:
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Ошибка")
                dlg.setText("Пользователь не найден!")
                dlg.exec()
            
    def ButtonRegPushed(self):
        if self.Reg is None:
            self.Reg = RW()
        self.Reg.show()


       
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
