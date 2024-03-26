import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox
from PyQt5.uic import loadUi

from models.user import initialize_databases, User, session

class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("login.ui", self)
        self.pushButton_login.clicked.connect(self.loginfunction)
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pushButton_signup.clicked.connect(self.gotosignup)

        # email alanı için doğrulayıcı ekleme
        email_validator= QRegExpValidator(QRegExp("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}"))
        self.lineEdit_email.setValidator(email_validator)

        # şifre için doğrulayıcı ekleme
        password_validator = QRegExpValidator(QRegExp(".{8,}"))
        self.lineEdit_password.setValidator(password_validator)

    def loginfunction(self):
        email = self.lineEdit_email.text()
        password = self.lineEdit_password.text()

        # email alanının doğruluğunu kontrol etme
        if not self.lineEdit_email.hasAcceptableInput():
            QMessageBox.warning(self, "Warning", "Invalid email format!")
            return

        # şifre alanının doğruluğunu kontrol etme
        if not self.lineEdit_password.hasAcceptableInput():
            QMessageBox.warning(self, "Warning", "Invalid password format! Password must be at least 8 characters long.")
            return

        # kullanıcıyı veritabanında sorgulama
        user = session.query(User).filter_by(email=email).first()
        if user:
            print("Successfully logged in with email: ", email, "and password: ", password)
        else:
            print("Login Failed!")


    def gotosignup(self):
        signup = SignUp()
        widget.addWidget(signup)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class SignUp(QDialog):
    def __init__(self):
        super(SignUp, self).__init__()
        loadUi("signup.ui", self)
        self.pushButton_signupui.clicked.connect(self.signupfunction)
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_confirmpassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pushButton_login.clicked.connect(self.gotologin)

        # email alanı için doğrulayıcı ekleme
        email_validator = QRegExpValidator(QRegExp("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}"))
        self.lineEdit_email.setValidator(email_validator)

        # şifre için doğrulayıcı ekleme
        password_validator = QRegExpValidator(QRegExp(".{8,}"))
        self.lineEdit_password.setValidator(password_validator)

    def signupfunction(self):
        username = self.lineEdit_username.text()
        email = self.lineEdit_email.text()
        if self.lineEdit_password.text() == self.lineEdit_confirmpassword.text():
            password = self.lineEdit_password.text()

            # email alanının doğruluğunu kontrol etme
            if not self.lineEdit_email.hasAcceptableInput():
                QMessageBox.warning(self, "Warning", "Invalid email format!")
                return

            # şifre alanının doğruluğunu kontrol etme
            if not self.lineEdit_password.hasAcceptableInput():
                QMessageBox.warning(self, "Warning", "Invalid password format! Password must be at least 8 characters long.")
                return

            # yeni kullanıcıyı veritabanına ekle
            new_user = User(username=username, email=email, password=password)
            session.add(new_user)
            session.commit()

            QMessageBox.information(self, "Success", "Successfully signed up!")
            login=Login()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex()+1)

    def gotologin(self):
        login=Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)

initialize_databases()
app=QApplication(sys.argv)
mainWindow=Login()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainWindow)
widget.setFixedWidth(480)
widget.setFixedHeight(620)
widget.show()
app.exec_()



"""import mysql.connector

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1")

mycursor = con.cursor()

mycursor.execute("CREATE DATABASE pythonProject")

from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)"""