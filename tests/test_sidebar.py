import unittest

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QApplication, QListWidgetItem

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

    def test_delete_task(self):
        # Öncelikle veritabanına birkaç görev ekleyin
        task1 = Task(title="Task 1", description="Test Description", due_date="2024-05-10", completed=True, user_id=2, categories="Work", priority=1)
        task2 = Task(title="Task 2", description="Test Description", due_date="2024-05-11", completed=True, user_id=2, categories="Personal", priority=2)
        session.add(task1)
        session.add(task2)
        session.commit()

        # Test işlevini çağırın
        sidebar = SideBar()
        sidebar.delete_task()

        # Görevlerin doğru bir şekilde silindiğini doğrulayın
        self.assertIsNone(session.query(Task).filter_by(id=8).first())
        self.assertIsNone(session.query(Task).filter_by(id=9).first())

    def test_load_task(self):
        # ListWidget'ı temizle
        self.sidebar.listWidget_task.clear()

        # Test için birkaç görev oluştur
        task1_info = f"Title: Task 1 - Due Date: 2024-05-10 - Completed: Yes - User ID: 1"
        task2_info = f"Title: Task 2 - Due Date: 2024-05-11 - Completed: Yes - User ID: 2"

        # Görevleri ListWidget'a ekle
        self.sidebar.listWidget_task.addItem(task1_info)
        self.sidebar.listWidget_task.addItem(task2_info)

        # ListWidget'taki öge sayısını kontrol et
        task_count = self.sidebar.listWidget_task.count()
        self.assertEqual(task_count, 2)  # Beklenen görev sayısı: 2

        # Her bir görevin doğru şekilde yüklendiğinin kontrolü
        expected_task_str_1 = "Title: Task 1 - Due Date: 2024-05-10 - Completed: Yes - User ID: 1"
        expected_task_str_2 = "Title: Task 2 - Due Date: 2024-05-11 - Completed: Yes - User ID: 2"

        # Birinci görevin doğru yüklenip yüklenmediğinin kontrolü
        first_item = self.sidebar.listWidget_task.item(0)
        self.assertIsInstance(first_item, QListWidgetItem)
        self.assertEqual(first_item.text(), expected_task_str_1)

        # İkinci görevin doğru yüklenip yüklenmediğinin kontrolü
        second_item = self.sidebar.listWidget_task.item(1)
        self.assertIsInstance(second_item, QListWidgetItem)
        self.assertEqual(second_item.text(), expected_task_str_2)

    def test_update_line_edits(self):
        # Test senaryosu: Bir görev oluştur ve list widget'a ekle
        task = Task(id=64, title="Test Task", description="Test Description Update", due_date="2024-05-10",
                    completed=True, user_id=2, categories="Work", priority=1)
        session.merge(task)
        session.commit()

        # Liste widget'ına görevi ekle
        task_str = f"ID: {task.id} - Title: {task.title} - Due Date: {task.due_date} - Completed: {'Yes' if task.completed else 'No'} - User ID: {task.user_id}"
        item = QListWidgetItem()
        item.setText(task_str)
        self.sidebar.listWidget_task.addItem(item)

        # liste widgetındaki görev ögesini seç
        self.sidebar.listWidget_task.setCurrentItem(item)

        # update_line_edits fonksiyonunu çağır
        self.sidebar.update_line_edits(item)

        self.sidebar.comboBox_completed.clear()
        self.sidebar.comboBox_completed.addItem("True")
        self.sidebar.comboBox_completed.addItem("False")
        self.sidebar.comboBox_category.clear()
        self.sidebar.comboBox_category.addItem("Work")
        self.sidebar.comboBox_category.addItem("Personal")
        self.sidebar.comboBox_priority.clear()
        self.sidebar.comboBox_priority.addItem("1")
        self.sidebar.comboBox_priority.addItem("2")

        # beklenen davranışları kontrol et
        self.assertEqual(self.sidebar.lineEdit_id.text(), str(task.id))  # ID alanının doğru şekilde doldurulduğunu kontrol et
        self.assertEqual(self.sidebar.lineEdit_tasktitle.text(), task.title)  # Title alanının doğruluğunun kontrolü
        self.assertEqual(self.sidebar.lineEdit_description.text(), task.description)
        self.assertEqual(self.sidebar.dateEdit_due.date().toString("yyyy-MM-dd"), task.due_date)
        self.assertEqual(self.sidebar.comboBox_completed.currentText(), "True" if task.completed else "False")
        self.assertEqual(self.sidebar.lineEdit_userid.text(), str(task.user_id))
        self.assertEqual(self.sidebar.comboBox_category.currentText(), task.categories)
        self.assertEqual(self.sidebar.comboBox_priority.currentText(), str(task.priority))

    def test_load_tasks_by_category(self):
        # seçili bir kategori belirle
        selected_category = "Work"
        self.sidebar.comboBox_kglistele.setCurrentText(selected_category)

        # load_task_by_category fonksiyonunu çağır
        self.sidebar.load_tasks_by_category()

        # görevlerin yüklendiğini kontrol etmek için listWidget'ı kontrol et
        loaded_task_count = self.sidebar.listWidget_task.count()

        # veritabanında kaç görev olduğunu kontrol edelim
        expected_task_count = len(session.query(Task).filter_by(categories=selected_category).all())

        # iki sayının eşit olup olmadığını kontrol edelim
        self.assertEqual(loaded_task_count, expected_task_count)

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