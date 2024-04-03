from sidebar_ui import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow

class SideBar(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('SideBar Menu')

        self.pushButton_home.clicked.connect(self.switch_to_page_home)
        self.pushButton_home2.clicked.connect(self.switch_to_page_home)

        self.pushButton_dashboard.clicked.connect(self.switch_to_page_dashboard)
        self.pushButton_dashboard2.clicked.connect(self.switch_to_page_dashboard)

        self.pushButton_users.clicked.connect(self.switch_to_page_users)
        self.pushButton_users2.clicked.connect(self.switch_to_page_users)

        self.pushButton_settings.clicked.connect(self.switch_to_page_settings)
        self.pushButton_settings2.clicked.connect(self.switch_to_page_settings)

    def switch_to_page_home(self):
        self.stackedWidget.setCurrentIndex(0)

    def switch_to_page_dashboard(self):
        self.stackedWidget.setCurrentIndex(1)

    def switch_to_page_users(self):
        self.stackedWidget.setCurrentIndex(2)

    def switch_to_page_settings(self):
        self.stackedWidget.setCurrentIndex(3)

