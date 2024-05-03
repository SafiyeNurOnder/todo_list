import unittest

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QApplication

from models import session
from models.task import Task
from sidebar import SideBar

# Sayfalar arasında geçiş işlevselliği
class TestSideBarPageSwitching(unittest.TestCase):

    def setUp(self):
        self.app = QApplication([])
        self.sidebar = SideBar()

    def test_switch_to_page_home(self):
        self.sidebar.switch_to_page_home() # switch_to_page_home metodunu çağırarak ana sayfaya geçiyor
        self.assertEqual(self.sidebar.stackedWidget.currentIndex(), 0) #stackedWidget mevut indexinin 0 olup olmadığının kontrolü

    def test_switch_to_page_dashboard(self):
        self.sidebar.switch_to_page_dashboard()
        self.assertEqual(self.sidebar.stackedWidget.currentIndex(), 1)

    def test_switch_to_page_addtask(self):
        self.sidebar.switch_to_page_addtask()
        self.assertEqual(self.sidebar.stackedWidget.currentIndex(), 2)

    def test_switch_to_page_settings(self):
        self.sidebar.switch_to_page_settings()
        self.assertEqual(self.sidebar.stackedWidget.currentIndex(), 3)

    def test_switch_to_page_search(self):
        self.sidebar.switch_to_page_search()
        self.assertEqual(self.sidebar.stackedWidget.currentIndex(), 4)

    def test_switch_to_page_profile(self):
        self.sidebar.switch_to_page_profile()
        self.assertEqual(self.sidebar.stackedWidget.currentIndex(), 5)

    def tearDown(self): # test sonunda temizlik işlemleri yapılıyor
        self.sidebar.close() # sidebar nesnesi kapatılıyor
        del self.sidebar # sidebar nesnesini silerek bellekten kaldırıyoruz
        del self.app # app nesnesini silerek bellekten kaldırıyoruz.

# Görev işlevselliği testleri
class TestSideBarTaskFunctionality(unittest.TestCase):

    def setUp(self):
        self.app = QApplication([])
        self.sidebar = SideBar()

    def test_add_task(self):
        # Test için gerekli widget'ların değerlerini ayarlayın
        self.sidebar.lineEdit_tasktitle.setText("Test Task")
        self.sidebar.lineEdit_description.setText("Test Description")
        self.sidebar.dateEdit_due.setDate(QDate.currentDate())
        self.sidebar.comboBox_completed.setCurrentText("Yes")
        self.sidebar.lineEdit_userid.setText("1")
        self.sidebar.comboBox_category.setCurrentText("Work")
        self.sidebar.comboBox_priority.setCurrentText("1")

        # 'session.query(Task).all()' ile tüm görevler sorgulanıp, görev sayısı 'initial_task_count' değişkenine atanıyor
        initial_task_count = len(session.query(Task).all()) # görev sayısını almadan önceki durumu al
        self.sidebar.add_task() #add_task metodunu çağırarak yeni görev ekliyoruz
        session.commit() # veritabanındaki değişiklikleri kaydet
        final_task_count = len(session.query(Task).all()) # görev sayısını aldıktan sonraki durum alınıyor

        self.assertEqual(final_task_count, initial_task_count + 1) # görev sayısının artıp artmadığının kontrolü

    # Diğer görev işlevselliği testleri de benzer şekilde oluşturulabilir

    def tearDown(self): # test sonunda temizlik işlemleri
        self.sidebar.close() # sidebar nesnesini kapat
        del self.sidebar # sidebar nesnesini silerek bellekten kaldırma
        del self.app # app nesnesini silerek bellekten kaldırma

# Arama işlevselliği testleri
class TestSideBarSearchFunctionality(unittest.TestCase):

    def setUp(self):
        self.app = QApplication([])
        self.sidebar = SideBar()

    def test_search_page(self):
        search_term = "home" # arama terimi belirlendi
        self.sidebar.lineEdit_search.setText(search_term) # 'lineEdit_search' widget'ına home değerini yazıyoruz. arama kutusuna bir terim girmilmiş olma durumunu simüle ediyor
        self.sidebar.search_page() # 'search_page()' metodu çağrılıyor ve bu metot arama kutusundaki terime göre bir sayfaya geçiş yapıyor
        self.assertEqual(self.sidebar.stackedWidget.currentIndex(), 0) # açılan sayfanın currentIndex'i 0 ise test başarılı

    def tearDown(self): # temizlik işlemleri
        self.sidebar.close()
        del self.sidebar
        del self.app

# Profil sayfasını yükleme işlevselliği test
class TestSideBarProfilePage(unittest.TestCase):

    def setUp(self):
        self.app = QApplication([])
        self.sidebar = SideBar()

    def test_profile_page(self):
        # Test için kullanıcı verisini ayarlayın
        self.sidebar.user_data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'testpass'} # user_data'yı kullanıcı verisi ile dolduruyoruz, gereken kullanıcı bilgileri simüle ediliyor
        self.sidebar.profile_page() # profile_page metodunu çağırarak profil sayfasını açıyoruz

        self.assertEqual(self.sidebar.lEdit_username.text(), 'testuser') #kullanıcı ad alanını kontrol ediyoruz
        self.assertEqual(self.sidebar.lEdit_email.text(), 'test@example.com') #kullanıcı email alanı kontrolü
        self.assertEqual(self.sidebar.lEdit_email.text(), 'testpass')  # Bu satırı düzeltebilirsiniz

    def tearDown(self):
        self.sidebar.close()
        del self.sidebar
        del self.app


if __name__ == '__main__': # ilgili durum sağlandığında 'unittest.main()' fonksiyonunu çağırarak testlerin çalışmasını sağlar.
    unittest.main()


""" kullanıcı oturum bilgilerini kontrol etme 
from unittest.mock import patch

class TestSideBarSessionCheck(unittest.TestCase):
    
    def setUp(self):
        self.app = QApplication([])
        self.sidebar = SideBar()

    @patch('PyQt5.QtCore.QSettings.value') # 'QSettings.value' metodunu mocklamak için 'unittest.mock.patch' dekoratörünü kullanır. böylece gerçek değer yerine mock bir değer döndürerek testi izole eder
    def test_check_sessions(self, mock_value): # 
        mock_value.return_value = {'username': 'testuser', 'email': 'test@example.com'} # metodun dönmesi gereken değer ayarlanıyor. kullanıcı adı, eposta adresi gibi oturum verileri simüle ediliyor
        self.sidebar.checkSessions() # 'checkSessions()' metodu çağrılarak oturum kontrolü başlatılır
        self.assertTrue(self.sidebar.showSidebarFunctionalities.called) # 'showSidebarFunctionalities' metodunun çağırılıp çağırılmadığı kontrol ediliyor, 'checkSession'  metodu içinde oturum kontrolü başarılıysa 2showSidebarFunctionalities' metodunun çağırılması gerekiyor

    def tearDown(self):
        self.sidebar.close()
        del self.sidebar
        del self.app
"""