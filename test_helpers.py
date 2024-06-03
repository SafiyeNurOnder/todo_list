import os
from PyQt5.QtWidgets import QApplication

def setup_qt_environment():
    if not QApplication.instance():
        os.environ['QT_QPA_PLATFORM'] = 'offscreen'
        app = QApplication([])
    return app