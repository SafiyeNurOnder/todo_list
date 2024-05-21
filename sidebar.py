from PyQt5.QtCore import QSettings

from models import session, user
from models.task import Task
from models.user import User
from sidebar_ui import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QListWidget, QVBoxLayout, QListWidgetItem

class SideBar(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('SideBar Menu')

        self.widget_icon_menu.hide()
        self.stackedWidget.setCurrentIndex(0)
        self.pushButton_home2.setChecked(True)

        # QSettings için anahtar ve uygulama adını ayarla
        # self.settings = QSettings("MySettings", "todoList")

        self.pushButton_home.clicked.connect(self.switch_to_page_home)
        self.pushButton_home2.clicked.connect(self.switch_to_page_home)

        self.pushButton_dashboard.clicked.connect(self.switch_to_page_dashboard)
        self.pushButton_dashboard2.clicked.connect(self.switch_to_page_dashboard)

        self.pushButton_addtask.clicked.connect(self.switch_to_page_addtask)
        self.pushButton_addtask2.clicked.connect(self.switch_to_page_addtask)

        self.pushButton_settings.clicked.connect(self.switch_to_page_settings)
        self.pushButton_settings2.clicked.connect(self.switch_to_page_settings)

        self.pushButton_search.clicked.connect(self.switch_to_page_search)

        self.pushButton_user.clicked.connect(self.switch_to_page_profile)

        self.pushButton_addtasksw.clicked.connect(self.add_task)
        self.pushButton_deletetask.clicked.connect(self.delete_task)
        self.pushButton_updatetask.clicked.connect(self.update_task)
        self.pushButton_listtask.clicked.connect(self.load_task)
        self.comboBox_kglistele.currentIndexChanged.connect(self.load_tasks_by_category)
        self.pushButton_search.clicked.connect(self.search_page)
        self.pButton_details.clicked.connect(self.profile_details)
        self.pushButton_deletetask_2.clicked.connect(self.delete_task2)
        self.pButton_logout.clicked.connect(self.close_and_open_homepage)

        self.pushButton_home2.clicked.connect(self.home_page)
        self.pushButton_addnew.clicked.connect(self.add_task_to_list)
        self.pButton_changepassword.clicked.connect(self.change_password)

        #self.pButton_details.clicked.connect(self.load_user)

    #def checkSessions(self): # QSettings ile ilgili eklemeler
        # Oturum bilgilerini QSettings'den yükle
        #from app import APP_ORG_NAME, APP_NAME, SETTINGS_KEY
        #settings = QSettings(APP_ORG_NAME, APP_NAME)
        #username = settings.value(SETTINGS_KEY + "/username")
        #email = settings.value(SETTINGS_KEY + "/email")

        #if username and email:
            # Oturum açık, sidebar işlevselliğini göster
            #self.showSidebarFunctionalities()
        #else:
            # Oturum açık değil, oturum açma sayfasına yönlendir
            #self.goToLogin()

    def switch_to_page_home(self):
        self.stackedWidget.setCurrentIndex(0)

    def switch_to_page_dashboard(self):
        self.stackedWidget.setCurrentIndex(1)

    def switch_to_page_addtask(self):
        self.stackedWidget.setCurrentIndex(2)

    def switch_to_page_settings(self):
        self.stackedWidget.setCurrentIndex(3)

    def switch_to_page_search(self):
        self.stackedWidget.setCurrentIndex(4)

    def switch_to_page_profile(self):
        self.stackedWidget.setCurrentIndex(5)

    def add_task(self):

        id = self.lineEdit_id.text().strip()
        title = self.lineEdit_tasktitle.text().strip()
        description = self.lineEdit_description.text().strip()
        due_date = self.dateEdit_due.date().toString("yyyy-MM-dd").strip()

        completed_text =self.comboBox_completed.currentText()
        completed = completed_text == 'Yes'

        user_id = self.lineEdit_userid.text().strip()
        categories = self.comboBox_category.currentText().strip()
        priority = self.comboBox_priority.currentText().strip()

        print(
            f"ID: {id}, Title: {title}, Description: {description}, Due Date: {due_date}, Completed: {completed}, User ID: {user_id}, Categories: {categories}, Priority: {priority}")

        if not (title.strip() and description.strip() and due_date.strip() and completed is not None and user_id.strip() and categories.strip() and priority.strip()):
            QMessageBox.warning(self, "Warning", "Relevant fields cannot be empty!")
            return

        new_task = Task(title=title, description=description, due_date=due_date, completed=completed,
                        categories=categories, priority=priority)

        if id:  # id boş değilse
            new_task.id = id
        if user_id:  # user_id boş değilse
            new_task.user_id = user_id

        session.add(new_task)
        session.commit()

        QMessageBox.information(self, "Information", "Quest added successfully!")

        self.lineEdit_id.clear()
        self.lineEdit_tasktitle.clear()
        self.lineEdit_description.clear()
        self.dateEdit_due.clear() # tekrar bakılacak
        self.comboBox_completed.setCurrentIndex(-1)
        self.lineEdit_userid.clear()
        self.comboBox_category.setCurrentIndex(-1)
        self.comboBox_priority.setCurrentIndex(-1)

    def delete_task(self):

        # Seçilen görevin bilgilerini al
        selected_item = self.listWidget_task.currentItem()
        if selected_item:
            task_info = selected_item.text()
            task_id = task_info.split(':')[1].split('-')[0].strip()

            # Veritabanından görevi sil
            task = session.query(Task).filter_by(id=task_id).first()
            if task:
                if task.description is not None:
                    session.delete(task)
                    session.commit()

                # ListWidget'tan seçilen öğeyi kaldır
                self.listWidget_task.takeItem(self.listWidget_task.currentRow())
                QMessageBox.information(self, "Information", "Task deleted successfully!")

    def update_task(self):

        # Seçilen görevin bilgilerini al
        selected_item = self.listWidget_task.currentItem()
        if selected_item:
            task_info = selected_item.text()
            task_id = task_info.split(':')[1].split('-')[0].strip()

            # Veritabanından seçilen görevi getir
            task = session.query(Task).filter_by(id=task_id).first()
            if task:
                # Görevin mevcut bilgilerini al
                current_title = task.title
                current_description = task.description
                current_due_date = task.due_date
                current_completed = task.completed
                current_user_id = task.user_id
                current_categories = task.categories
                current_priority = task.priority

                # Yeni bilgileri LineEdit ve ComboBox widget'larından al
                new_title = self.lineEdit_tasktitle.text()
                new_description = self.lineEdit_description.text()
                new_due_date = self.dateEdit_due.date().toPyDate()
                new_completed = self.comboBox_completed.currentText() == 'Yes'
                new_user_id = int(self.lineEdit_userid.text())
                new_categories = self.comboBox_category.currentText()
                new_priority = int(self.comboBox_priority.currentText())

                # Değişiklik kontrolü yap
                if (new_title != current_title or
                        new_description != current_description or
                        new_due_date != current_due_date or
                        new_completed != current_completed or
                        new_user_id != current_user_id or
                        new_categories != current_categories or
                        new_priority != current_priority):

                    # Değişiklik varsa güncelle
                    task.title = new_title
                    task.description = new_description
                    task.due_date = new_due_date
                    task.completed = new_completed
                    task.user_id = new_user_id
                    task.categories = new_categories
                    task.priority = new_priority

                    session.commit()

                    # ListWidget'ta görevi güncelle
                    updated_task_str = f"ID: {task.id} - Title: {task.title} - Due Date: {new_due_date.strftime('%Y-%m-%d')} - Completed: {'Yes' if new_completed else 'No'} - User ID: {task.user_id}"
                    selected_item.setText(updated_task_str)

                    QMessageBox.information(self, "Information", "Task updated successfully!")
                else:
                    QMessageBox.warning(self, "Warning", "No changes detected!")

    def load_task(self):

        # Mevcut görevleri temizle
        self.listWidget_task.clear()

        # Veritabanından tüm görevleri çek
        tasks = session.query(Task).all()

        # Her görev için ListWidget'a öğe ekleyin
        for task in tasks:
            completed_status = 'Yes' if task.completed else 'No'
            due_date_str = task.due_date.strftime("%Y-%m-%d")
            task_str = f"ID: {task.id} - Title: {task.title} - Due Date: {due_date_str} - Completed: {completed_status} - User ID: {task.user_id}"
            self.listWidget_task.addItem(task_str)

        # ListWidget'dan bir öğe seçildiğinde tetiklenecek fonksiyonu bağlayın
        self.listWidget_task.itemClicked.connect(self.update_line_edits)

    def update_line_edits(self, item):
        task_info = item.text()
        task_id = task_info.split(':')[1].split('-')[0].strip()

        # Veritabanından seçilen görevi getir
        task = session.query(Task).filter_by(id=task_id).first()
        if task:
            # Görevin bilgilerini LineEdit ve ComboBox widget'larına yükle
            self.lineEdit_id.setText(str(task.id))
            self.lineEdit_tasktitle.setText(task.title)
            self.lineEdit_description.setText(task.description)
            self.dateEdit_due.setDate(task.due_date)
            if task.completed:
                self.comboBox_completed.setCurrentText('Yes')
            else:
                self.comboBox_completed.setCurrentText('No')
            self.lineEdit_userid.setText(str(task.user_id))
            self.comboBox_category.setCurrentText(task.categories)
            self.comboBox_priority.setCurrentText(str(task.priority))

    def load_tasks_by_category(self):

        # Mevcut görevleri temizle
        self.listWidget_task.clear()

        # Seçilen kategoriyi al
        selected_category = self.comboBox_kglistele.currentText()

        # Veritabanından seçilen kategoriye ait görevleri çek
        tasks = session.query(Task).filter_by(categories=selected_category).all()

        # Her görev için ListWidget'a öğe ekleyin
        for task in tasks:
            completed_status = 'Yes' if task.completed else 'No'
            due_date_str = task.due_date.strftime("%Y-%m-%d")
            task_str = f"ID: {task.id} - Title: {task.title} - Due Date: {due_date_str} - Completed: {completed_status} - User ID: {task.user_id}"
            self.listWidget_task.addItem(task_str)

    def search_page(self):
        search_text = self.lineEdit_search.text().strip()
        if not search_text:
            QMessageBox.warning(self, "Warning", "Please enter a search term!")
            return

        # Arama sonuçlarına göre hangi sayfaya geçileceğini belirleyin.
        if 'home' in search_text.lower():
            self.stackedWidget.setCurrentIndex(0)
        elif 'dashboard' in search_text.lower():
            self.stackedWidget.setCurrentIndex(1)
        elif 'add task' in search_text.lower():
            self.stackedWidget.setCurrentIndex(2)
        elif 'settings' in search_text.lower():
            self.stackedWidget.setCurrentIndex(3)
        elif 'profile' in search_text.lower():
            self.stackedWidget.setCurrentIndex(5)
        else:
            QMessageBox.warning(self, "Warning", "No matching page found!")

    def profile_details(self, item):
        if item is not None:

            # Veritabanından seçilen kullanıcıyı getir
            user = session.query(User).filter_by(id=2).first()
            if user:
                # Kullanıcı bilgilerini LineEdit widget'larına yükle
                self.lEdit_username.setText(user.username)
                self.lEdit_username.setReadOnly(True)
                self.lEdit_email.setText(user.email)
                self.lEdit_email.setReadOnly(True)
                self.lEdit_password.setPlaceholderText(user.password) # bu şekilde arka planda görünmeye devam ediyor yeni bir metin girilebilir durumda

    def change_password(self):
        user = session.query(User).filter_by(id=2).first()
        if user:
            # Görevin mevcut bilgilerini al
            current_password = user.password

            # Yeni bilgileri LineEdit ve ComboBox widget'larından al
            new_password = self.lEdit_password.text()

            # Değişiklik kontrolü yap
            if (new_password != current_password):

                # Değişiklik varsa güncelle
                user.password = new_password

                session.commit()

                QMessageBox.information(self, "Information", "Password updated successfully!")
            else:
                QMessageBox.warning(self, "Warning", "No changes detected!")
        else:
            QMessageBox.warning(self, "Warning", "Please enter a new password!")

    #def profile_page(self, username):
        # Kullanıcı adına göre veritabanından kullanıcıyı getir
        #user = session.query(User).filter_by(username=username).first()
        #if user:
            # Kullanıcı bilgilerini LineEdit widget'larına yükle
            #self.lEdit_username.setText(user.username)
            #self.lEdit_email.setText(user.email)
            #self.lEdit_password.setText(user.password)
        #else:
            #QMessageBox.warning(self, "Warning", "User not found")

    def close_and_open_homepage(self):
        self.close()  # Sayfayı kapat

    def home_page(self):
        # ComboBox zaten doluysa tekrar yükleme
        if self.comboBox_addnewtask.count() > 0:
            return

        # Veritabanından tüm görev başlıklarını çek
        tasks = session.query(Task.title).all()

        # Görev başlıklarını ComboBox'a ekleyin
        for task in tasks:
            self.comboBox_addnewtask.addItem(task.title)

    def delete_task2(self):
        # Seçilen görevin bilgilerini al
        selected_item = self.listWidget.currentItem()
        if selected_item:
            # Seçilen öğenin sadece text bilgisini al
            task_info = selected_item.text()
            task_id = task_info.split(':')[1].split('-')[0].strip()

            # Seçilen öğenin text bilgisini list widget'tan kaldır
            self.listWidget.takeItem(self.listWidget.currentRow())

            # List widget'ın görünümünü güncelle
            self.listWidget.update()  # veya .repaint()

    def add_task_to_list(self):
        # Seçilen görevi al
        selected_task = self.comboBox_addnewtask.currentText()

        # Seçilen tarihi al
        selected_date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")

        # Görev ve tarih bilgisini birleştir
        task_info = f"Task: {selected_task} - Due Date: {selected_date}"

        # Liste öğesi oluştur ve görev bilgisi ile ayarla
        item = QListWidgetItem()
        item.setText(task_info)

        # ListeWidget'a öğeyi ekle
        self.listWidget.addItem(item)