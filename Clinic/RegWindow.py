from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *
from DatabaseHandler import Database_connect, insert_user, insert_doctor, insert_expert, create_question_list, insert_patient

class RW(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Регистрация")
        self.setFixedSize(QSize(300, 400))
        
        loginLayout = QHBoxLayout()
        self.loginLabel = QLabel("Логин:")
        self.passwordLabel = QLabel("Парол:")
        self.ageLabel = QLabel("Возр.:")
        self.occupationLabel = QLabel("Проф.:")
        self.nameLabel = QLabel("Имя:")
        self.lastNameLabel = QLabel("Фам.:")

        buttonReg = QPushButton("Регистрация")
        buttonBack = QPushButton("Назад")
        
        self.loginInput = QLineEdit("")
        self.passwordInput = QLineEdit("")
        self.passwordInput.setEchoMode(QLineEdit.Password)
        self.ageInput = QLineEdit("")
        self.occupationInput = QComboBox()
        self.occupationInput.setPlaceholderText("")
        self.occupationInput.addItems(["Пациент", "Врач", "Администратор", "Эксперт"])
        self.nameInput = QLineEdit("")
        self.lastNameInput = QLineEdit("")

        pageLayout = QVBoxLayout()
        loginLayout = QHBoxLayout()
        passwordLayout = QHBoxLayout()
        ageLayout = QHBoxLayout()
        buttonLayout = QHBoxLayout()
        occupationLayout = QHBoxLayout()
        nameLayout = QHBoxLayout()
        lastNameLayout =QHBoxLayout()

        loginLayout.addWidget(self.loginLabel)
        loginLayout.addWidget(self.loginInput)
        passwordLayout.addWidget(self.passwordLabel)
        passwordLayout.addWidget(self.passwordInput)
        ageLayout.addWidget(self.ageLabel)
        ageLayout.addWidget(self.ageInput)
        occupationLayout.addWidget(self.occupationLabel)
        occupationLayout.addWidget(self.occupationInput)
        nameLayout.addWidget(self.nameLabel)
        nameLayout.addWidget(self.nameInput)
        lastNameLayout.addWidget(self.lastNameLabel)
        lastNameLayout.addWidget(self.lastNameInput)
        buttonLayout.addWidget(buttonReg)
        buttonLayout.addWidget(buttonBack)

        pageLayout.addLayout(nameLayout)
        pageLayout.addLayout(lastNameLayout)
        pageLayout.addLayout(ageLayout)
        pageLayout.addLayout(loginLayout)
        pageLayout.addLayout(passwordLayout)
        pageLayout.addLayout(occupationLayout)
        pageLayout.addLayout(buttonLayout)

        self.setLayout(pageLayout)

        buttonReg.clicked.connect(self.ButtonRegPushed)
        buttonBack.clicked.connect(self.ButtonBackPushed)

    def ButtonRegPushed(self):
        if (self.loginInput.text()=='')or(self.passwordInput.text()=='')or(self.nameInput.text()=='')or(self.lastNameInput.text()=='')or(self.ageInput.text()==''):
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Поля пусты!")
                dlg.setText("Не все поля заполнены!")
                dlg.exec()
        else:
            insert_user(self.loginInput.text(),
                        self.passwordInput.text(),
                        self.nameInput.text(),
                        self.lastNameInput.text(),
                        self.ageInput.text(),
                        self.occupationInput.currentText())
            if self.occupationInput.currentText()=="Врач":
                insert_doctor(self.nameInput.text(),
                              self.lastNameInput.text(),
                              self.ageInput.text())
            elif self.occupationInput.currentText()=="Эксперт":
                insert_expert(self.nameInput.text(),
                              self.lastNameInput.text(),
                              self.ageInput.text())
            elif self.occupationInput.currentText()=="Пациент":
                insert_patient(self.nameInput.text(),
                               self.lastNameInput.text(),
                               self.ageInput.text(),
                               "")
                PrSt = Database_connect()
                with PrSt.cursor() as cursor:
                    find_patient_id_query = "SELECT idpatients FROM patients WHERE name=%s AND lastname=%s AND age=%s"
                    cursor.execute(find_patient_id_query, (self.nameInput.text(), self.lastNameInput.text(), self.ageInput.text()))
                result = cursor.fetchone()
                create_question_list(result['idpatients'])
        self.close()

    def ButtonBackPushed(self):
        self.close()
 

        

        
        
            
        


