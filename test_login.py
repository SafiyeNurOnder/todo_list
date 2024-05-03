import unittest
from unittest.mock import patch, MagicMock

from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QMessageBox

from login import Login


class test_login(unittest.TestCase):

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

        if __name__ == '__main__':
            unittest.main()




"""
import unittest
from unittest.mock import patch, MagicMock

from PyQt5.QtWidgets import QApplication
from login import Login

app = QApplication([])

class TestLogin(unittest.TestCase):

    def setUp(self): # 'setup' her test metodu çalıştırılmadan önce çalışır, özellikle testlerde kullanılacak nesneler veya verilerin başlatılması için
        self.login = Login()

    def test_email_validation(self):
        # Geçersiz e-posta formatı
        self.login.lineEdit_email.setText("invalid_email") #!!!
        self.assertFalse(self.login.lineEdit_email.hasAcceptableInput()) # assertX, testin başarılı olup olamdığını kontrol eder

        # Geçerli e-posta formatı
        self.login.lineEdit_email.setText("valid_email@example.com") #!!!
        self.assertTrue(self.login.lineEdit_email.hasAcceptableInput()) # assertX, testin başarılır olup olamdığını kontrol eder

    def test_password_validation(self):
        # Geçersiz şifre formatı
        self.login.lineEdit_password.setText("pass") #!!!
        self.assertFalse(self.login.lineEdit_password.hasAcceptableInput()) # hasAcceptableInput(), widget içeriğinin kabul edilebilir bir değer olup olmadığını kabul eder

        # Geçerli şifre formatı
        self.login.lineEdit_password.setText("validpassword") #!!!
        self.assertTrue(self.login.lineEdit_password.hasAcceptableInput())

    # Test için mock bir user oluşturarak kullanıcı girişi testi yapabiliriz

# unittest.mock.patch modülü, Python'un unittest kütüphanesiyle birlikte kullanıldığında oldukça güçlü bir mocklama aracıdır. Mocklama, gerçek sistem çağrılarını ve objeleri taklit ederek testlerde kullandığımız veriyi kontrol etmemizi ve izole testler yazmamızı sağlar.
    @patch('login.session.query') #Bir fonksiyonun veya metodun gerçek davranışını geçici olarak değiştirmek için patch fonksiyonunu kullanırız.
    def test_login_function(self, mock_query):
        # Mock kullanıcı oluşturma, unittest.mock modülü, testlerde mock objeler ve fonksiyonlar oluşturmak için kullanılır. Özellikle harici servislerle veya veritabanıyla çalışırken gerçek veri kullanmak yerine simüle veri veya işlemler yapmak için kullanılır.
        mock_user = MagicMock()
        mock_user.email = "valid_email@example.com"
        mock_user.password = "validpassword"

        mock_query.return_value.filter_by.return_value.first.return_value = mock_user #bir SQLAlchemy query sorgusunu (mock_query) mocklamaktadır. Bu mock sorgu, filter_by metoduna çağrıldığında belirli bir değeri (genellikle bir sorgu kriteri) ve first metoduna çağrıldığında belirli bir kullanıcı nesnesini döndürmek üzere ayarlanmıştır. Bu sayede gerçek bir veritabanına bağlanmadan, testlerinizi simüle edilmiş verilerle yapabilirsiniz.

        self.login.lineEdit_email.setText("valid_email@example.com")
        self.login.lineEdit_password.setText("validpassword")

        self.login.loginfunction()

        # Test için ekranda yeni bir widget (sidebar) oluşturulmuş mu diye kontrol ediyoruz
        from app import widget
        self.assertEqual(widget.currentIndex(), 1)  # Eğer sidebar eklenmişse index 1 olmalı

if __name__ == '__main__':
    unittest.main()

# unittest.main() fonksiyonu ile testleri komut satırından çalıştırabiliriz. Ek argümanlar da kullanılabilir.
# -v veya --verbose: Test sonuçlarını detaylı bir şekilde gösterir.
# -f veya --failfast: İlk başarısız olan testte durur.
# -s: Test dosyalarının veya dizinlerin adlarını belirtir.

# python -m unittest -v test_module.py

# tearDown(): Her test metodu çalıştırıldıktan sonra çalıştırılan metoddur. Kullanılan nesnelerin veya verilerin temizlenmesi için kullanılır."""