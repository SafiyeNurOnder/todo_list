"""
import unittest
from PyQt5.QtWidgets import QApplication, QLineEdit, QMessageBox
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from signup import SignUp


class TestSignUp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance()
        if cls.app is None:
            cls.app = QApplication([])

    @classmethod
    def tearDownClass(cls):
        cls.app.exit()

    def setUp(self):
        self.window = SignUp()
        self.window.show()

    def tearDown(self):
        self.window.close()

    def test_empty_fields(self):
        self.window.lineEdit_username.setText('')
        self.window.lineEdit_email.setText('')
        self.window.lineEdit_password.setText('')
        self.window.lineEdit_confirmpassword.setText('')

        self.window.signupfunction()
        self.assertEqual(self.window.isVisible(), True)
        self.assertEqual(self.window.findChild(QMessageBox).text(), "Please fill all fields!")

    def test_invalid_email(self):
        self.window.lineEdit_username.setText('testuser')
        self.window.lineEdit_email.setText('invalid_email')
        self.window.lineEdit_password.setText('testpass')
        self.window.lineEdit_confirmpassword.setText('testpass')

        self.window.signupfunction()
        self.assertEqual(self.window.isVisible(), True)
        self.assertEqual(self.window.findChild(QMessageBox).text(), "Invalid email format!")

    def test_invalid_password(self):
        self.window.lineEdit_username.setText('testuser')
        self.window.lineEdit_email.setText('testuser@example.com')
        self.window.lineEdit_password.setText('pass')
        self.window.lineEdit_confirmpassword.setText('pass')

        self.window.signupfunction()
        self.assertEqual(self.window.isVisible(), True)
        self.assertEqual(self.window.findChild(QMessageBox).text(),
                         "Invalid password format! Password must be at least 8 characters long.")

    def test_successful_signup(self):
        self.window.lineEdit_username.setText('testuser')
        self.window.lineEdit_email.setText('testuser@example.com')
        self.window.lineEdit_password.setText('testpassword')
        self.window.lineEdit_confirmpassword.setText('testpassword')

        self.window.signupfunction()
        QTest.qWaitForWindowExposed(self.window)
        self.assertEqual(self.window.isVisible(), False)
        self.assertEqual(self.window.findChild(QMessageBox).text(), "Successfully signed up!")


if __name__ == "__main__":
    unittest.main()

"""