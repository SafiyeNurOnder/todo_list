import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

from login import Login

# QSettings ile ilgili eklemeler
# Uygulama ve ayar anahtarları
APP_ORG_NAME = "MyApp"
APP_ORG_DOMAIN = "myapp.com"
APP_NAME = "MyApp"
SETTINGS_KEY = "UserSettings"

app=QApplication(sys.argv)
mainWindow=Login()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainWindow)
widget.show()
app.exec_()
