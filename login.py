from PyQt5 import QtWidgets
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi

from models import session
from models.user import User


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

        # kullanıcıyı veritabanında sorgulama - READ
        user = session.query(User).filter_by(email=email).first()

        # bu kısım olunca if bloğu çalıştı. (şifre db'de byte dizisi olarak saklanıyor. kullanıcın girdiği şifre ile doğrudan karşılaştırılamaz)
        print(f"Email: {email}")
        print(f"User from DB: {user}")
        if user:
            print(f"User ID: {user.id}")
            print(f"User Email: {user.email}")
            print(f"User Password: {user.password}")

        # Şifreleri byte dizisine dönüştürme
        password_bytes = password.encode('utf-8')

        if user and user.password == password_bytes:
            QMessageBox.information(self, "Success", "Login successful!")
            self.gotosidebar()
        else:
            QMessageBox.warning(self, "Warning", "Login Failed!")


    def gotosignup(self):
        from signup import SignUp
        signup = SignUp()
        from app import widget
        widget.addWidget(signup)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotosidebar(self):
        from sidebar import SideBar
        sidebar = SideBar()
        from app import widget
        widget.addWidget(sidebar)
        widget.setCurrentIndex(widget.currentIndex()+1)