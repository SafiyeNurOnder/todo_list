import unittest
from unittest.mock import patch
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtTest import QTest
from signup import SignUp
from models.user import User
from models import session
#from test_helpers import setup_qt_environment

app = QApplication([]) # Yeni bir QApplication örneği oluşturur.

class TestSignUp(unittest.TestCase): # unittest.TestCase sınıfından türetilmiş bir test sınıfıdır.

    #@classmethod
    #def setUpClass(cls):
        #cls.app = setup_qt_environment()

    @classmethod # Sınıf seviyesinde bir setUp metodu. QApplication örneğini oluşturur veya mevcut bir örneği alır.
    def setUpClass(cls):
        cls.app = QApplication.instance()
        if cls.app is None:
            cls.app = QApplication([])

    @classmethod # Sınıf seviyesinde bir tearDown metodu. Uygulamayı kapatır.
    def tearDownClass(cls):
        cls.app.exit()

    def setUp(self): # Her test metodu başlamadan önce çalışacak olan setUp metodu. SignUp penceresini oluşturur ve gösterir.
        self.window = SignUp()
        self.window.show()

    def tearDown(self): # Her test metodu bittikten sonra çalışacak olan tearDown metodu. SignUp penceresini kapatır.
        self.window.close()


    @patch('signup.session.add')
    @patch('signup.session.commit')
    def test_signup_valid(self, mock_commit, mock_add): # signup modülünden session.add ve session.commit fonksiyonlarını mocklar. Gerçek veritabanına erişmeden test yapabilmek için.
        self.window.lineEdit_username.setText("test_user")
        self.window.lineEdit_email.setText("test_user@example.com")
        self.window.lineEdit_password.setText("password")
        self.window.lineEdit_confirmpassword.setText("password")

        self.window.signupfunction()

        # Veritabanına kullanıcının eklenip eklenmediğini kontrol etme
        mock_add.assert_called()
        mock_commit.assert_called()

    @patch('signup.QMessageBox.warning')
    def test_empty_fields(self, mock_warning): # signup modülünden QMessageBox.warning fonksiyonunu mocklar. Boş alanlarla ilgili uyarı mesajının doğru çağrılıp çağrılmadığını kontrol eder.
        self.window.lineEdit_username.setText("")
        self.window.lineEdit_email.setText("")
        self.window.lineEdit_password.setText("")
        self.window.lineEdit_confirmpassword.setText("")

        self.window.signupfunction()

        # QMessageBox.warning'in çağrılıp çağrılmadığını ve doğru mesajla çağrıldığını kontrol etme
        mock_warning.assert_called_with(self.window, "Warning", "Please fill all fields!")

    @patch('signup.QMessageBox.warning')
    def test_invalid_email(self, mock_warning):
        self.window.lineEdit_username.setText("testuser")
        self.window.lineEdit_email.setText("invalid_email")
        self.window.lineEdit_password.setText("testpass")
        self.window.lineEdit_confirmpassword.setText("testpass")

        self.window.signupfunction()

        # QMessageBox.warning'in çağrılıp çağrılmadığını ve doğru mesajla çağrıldığını kontrol etme
        mock_warning.assert_called_with(self.window, "Warning", "Invalid email format!")

    @patch('signup.QMessageBox.warning')
    def test_invalid_password(self, mock_warning):
        self.window.lineEdit_username.setText("testuser")
        self.window.lineEdit_email.setText("testuser@example.com")
        self.window.lineEdit_password.setText("pass")
        self.window.lineEdit_confirmpassword.setText("pass")

        self.window.signupfunction()

        # QMessageBox.warning'in çağrılıp çağrılmadığını ve doğru mesajla çağrıldığını kontrol etme
        mock_warning.assert_called_with(self.window, "Warning", "Invalid password format! Password must be at least 8 characters long.")

    @patch('signup.QMessageBox.information')
    def test_successful_signup(self, mock_info):
        self.window.lineEdit_username.setText("testuser")
        self.window.lineEdit_email.setText("testuser@example.com")
        self.window.lineEdit_password.setText("testpassword")
        self.window.lineEdit_confirmpassword.setText("testpassword")

        self.window.signupfunction()
        QTest.qWait(1000) #1 sn bekle
        #QTest.qWaitForWindowExposed(self.window) # pencerenin görünür hale gelmesini bekler

        # QMessageBox.information'ın çağrılıp çağrılmadığını ve doğru mesajla çağrıldığını kontrol etme
        mock_info.assert_called_with(self.window, "Success", "Successfully signed up!")


if __name__ == "__main__": # Eğer bu dosya doğrudan çalıştırılıyorsa (import edilmiyorsa), unittest'in main metodu çalıştırılır ve testler başlatılır.
    unittest.main()

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