import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

from login import Login

app=QApplication(sys.argv)
mainWindow=Login()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainWindow)
widget.show()
app.exec_()
