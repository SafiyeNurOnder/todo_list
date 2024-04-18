import unittest
from unittest.mock import patch, MagicMock

from PyQt5.QtWidgets import QApplication
from login import Login

app = QApplication([])


class TestLogin(unittest.TestCase):

    def setUp(self):
        self.login = Login()

    def test_email_validation(self):
        # Geçersiz e-posta formatı
        self.login.lineEdit_email.setText("invalid_email") #!!!
        self.assertFalse(self.login.lineEdit_email.hasAcceptableInput())

        # Geçerli e-posta formatı
        self.login.lineEdit_email.setText("valid_email@example.com") #!!!
        self.assertTrue(self.login.lineEdit_email.hasAcceptableInput())

    def test_password_validation(self):
        # Geçersiz şifre formatı
        self.login.lineEdit_password.setText("pass") #!!!
        self.assertFalse(self.login.lineEdit_password.hasAcceptableInput())

        # Geçerli şifre formatı
        self.login.lineEdit_password.setText("validpassword") #!!!
        self.assertTrue(self.login.lineEdit_password.hasAcceptableInput())

    # Test için mock bir user oluşturarak kullanıcı girişi testi yapabiliriz

    @patch('login.session.query')
    def test_login_function(self, mock_query):
        # Mock kullanıcı oluşturma
        mock_user = MagicMock()
        mock_user.email = "valid_email@example.com"
        mock_user.password = "validpassword"

        mock_query.return_value.filter_by.return_value.first.return_value = mock_user

        self.login.lineEdit_email.setText("valid_email@example.com")
        self.login.lineEdit_password.setText("validpassword")

        self.login.loginfunction()

        # Test için ekranda yeni bir widget (sidebar) oluşturulmuş mu diye kontrol ediyoruz
        from app import widget
        self.assertEqual(widget.currentIndex(), 1)  # Eğer sidebar eklenmişse index 1 olmalı

if __name__ == '__main__':
    unittest.main()