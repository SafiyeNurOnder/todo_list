from PyQt5 import QtWidgets
from PyQt5.QtCore import QRegExp, QSettings
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi

from models import session
from models.user import User

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

            # Alanların doluluğunu kontrol etme
            if not (username and email and password):
                QMessageBox.warning(self, "Warning", "Please fill all fields!")
                return

            # email alanının doğruluğunu kontrol etme
            if not self.lineEdit_email.hasAcceptableInput():
                QMessageBox.warning(self, "Warning", "Invalid email format!")
                return

            # şifre alanının doğruluğunu kontrol etme
            if not self.lineEdit_password.hasAcceptableInput():
                QMessageBox.warning(self, "Warning", "Invalid password format! Password must be at least 8 characters long.")
                return

            # yeni kullanıcıyı veritabanına ekle - CREATE
            new_user = User(username=username, email=email, password=password)
            session.add(new_user)
            session.commit()

            # QSettings ile ilgili eklemeler
            # Oturum bilgilerini QSettings ile sakla
            from app import APP_ORG_NAME, APP_NAME, SETTINGS_KEY
            settings = QSettings(APP_ORG_NAME, APP_NAME)
            settings.setValue(SETTINGS_KEY + "/username", new_user.username)
            settings.setValue(SETTINGS_KEY + "/email", new_user.email)

            QMessageBox.information(self, "Success", "Successfully signed up!")
            self.gotologin()

            from app import widget
            QMessageBox.information(self, "Success", "Successfully signed up!")
            from login import Login
            login=Login()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex()+1)

    #def gotologin(self):
        #from login import Login
        #from app import widget
        #login=widget()
        #widget.addWidget(login)
        #widget.setCurrentIndex(widget.currentIndex()+1)

    def gotologin(self):
        from login import Login
        login=Login()
        self.widget.addWidget(login)
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)