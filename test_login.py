import unittest
from unittest.mock import patch, MagicMock

#import xmlrunner
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QMessageBox

from login import Login
#from test_helpers import setup_qt_environment


class test_login(unittest.TestCase):

    #@classmethod
    #def setUpClass(cls):
        #cls.app = setup_qt_environment()

    def setUp(self):
        self.login = Login()

    def test_valid_login(self):
        #
        with patch('login.session.query') as mock_query:
            #
            mock_user = MagicMock()
            mock_user.email = 'valid_email@example.com'
            mock_user.password = 'validpassword'
            mock_query.return_value.filter_by.return_value.first.return_value = mock_user

            self.login.lineEdit_email.setText('valid_email@example.com')
            self.login.lineEdit_password.setText('validpassword')

            QTest.mouseClick(self.login.pushButton_login, Qt.LeftButton)

            self.assertEqual(self.login.gotosidebar.call_count, 1)
            self.assertEqual(QMessageBox.information.call_count, 1)
            self.assertEqual(QMessageBox.information.call_args[0][2], "Login successful!")

        def test_invalid_email_login(self):

            self.login.lineEdit_email.setText('invalid_email')
            self.login.lineEdit_password.setText('validpassword')

            QTest.mouseClick(self.login.pushButton_login, Qt.LeftButton)

            self.assertEqual(QMessageBox.warning.call_count, 1)
            self.assertEqual(QMessageBox.warning.call_args[0][2], "Invalid email format!")


        def test_invalid_password_login(self):

            self.login.lineEdit_email.setText('valid_email@example.com')
            self.login.lineEdit_password.setText("pass")

            QTest.mouseClick(self.login.pushButton_login, Qt.LeftButton)

            self.assertEqual(QMessageBox.warning.call_count, 1)
            self.assertEqual(QMessageBox.warning.call_args[0][2], "Invalid password format! Password must be at least 8 characters long.")

        def test_wrong_credentials_login(self):

            with patch('login.session.query') as mock_query:

                mock_user = MagicMock()
                mock_user.email = 'valid_email@example.com'
                mock_user.password = 'validpassword'
                mock_query.return_value.filter_by.return_value.first.return_value = mock_user

                self.login.lineEdit_email.setText('valid_email@example.com')
                self.login.lineEdit_password.setText("wrongpassword")

                QTest.mouseClick(self.login.pushButton_login, Qt.LeftButton)

                self.assertEqual(QMessageBox.warning.call_count, 1)
                self.assertEqual(QMessageBox.warning.call_args[0][2], "Login Failed!")

        #if __name__ == '__main__':
            #unittest.main ()

    #if __name__ == '__main__':
        #with open('tests/reports/results.xml', 'w') as output:
            #unittest.main(testRunner=xmlrunner.XMLTestRunner(output=output))


# unittest.main() fonksiyonu ile testleri komut satırından çalıştırabiliriz. Ek argümanlar da kullanılabilir.
# -v veya --verbose: Test sonuçlarını detaylı bir şekilde gösterir.
# -f veya --failfast: İlk başarısız olan testte durur.
# -s: Test dosyalarının veya dizinlerin adlarını belirtir.

# python -m unittest -v test_module.py

# tearDown(): Her test metodu çalıştırıldıktan sonra çalıştırılan metoddur. Kullanılan nesnelerin veya verilerin temizlenmesi için kullanılır."""