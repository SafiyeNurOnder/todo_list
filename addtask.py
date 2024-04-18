import sys

from PyQt5.uic import loadUi

from sidebar_ui import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication

from models import session
from models.task import Task


class AddTask(QMainWindow):
    def __init__(self):
        super(AddTask, self).__init__()
        # Load the UI file
        loadUi('mainwindow.ui', self)

        # Connect button click to a function
        self.pushButton_addtasksw.clicked.connect(self.on_button_click)

    def on_button_click(self):
        # Define the action to perform when the button is clicked
        print("Button clicked!")
        # Add your desired action here

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AddTask()
    window.show()
    sys.exit(app.exec_())

"""
class AddTask(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("AddTask Menu")
        self.pushButton_addtasksw.clicked.connect(self.add_task)
        #self.pushButton_deletetask.clicked.connect(self.delete_task)
        #self.pushButton_listtask.clicked.connect(self.load_task)

    def add_task(self):
        id = self.lineEdit_id.text()
        title = self.lineEdit_tasktitle.text()
        description = self.lineEdit_description.text()
        due_date = self.dateEdit_due.date().toString("yyyy-MM-dd")
        completed = self.combobox_completed.currentText()
        user_id = self.lineEdit_userid.text()
        categories = self.comboBox_category.currentText()
        priority = self.comboBox_priority.currentText()

        if not (id and title and description and due_date and completed and user_id and categories and priority):
            QMessageBox.warning(self, "Warning", "Relevant fields cannot be empty!")
            return

        new_task = Task(id=id, title=title, description=description, due_date=due_date, completed=completed, user_id=user_id, categories=categories, priority=priority)
        session.add(new_task)
        session.commit()

        QMessageBox.information(self, "Information", "Quest added successfully!")

        self.lineEdit_id.clear()
        self.lineEdit_tasktitle.clear()
        self.lineEdit_description.clear()
        self.dateEdit_due.clear()
        self.comboBox_completed.setCurrentIndex(-1)
        self.lineEdit_user_id.clear()
        self.comboBox_category.setCurrentIndex(-1)
        self.comboBox_priority.setCurrentIndex(-1)
"""
"""
    def delete_task(self):
        selected_item = self.taskList.currentItem()

        if not selected_item:
            QMessageBox.warning(self, "Warning", "Please select the task you want to delete!")
            return

            # Görevi veritabanından sil
        task_text = selected_item.text()
        username, task_name = task_text.split(",")[0].split(":")[1].strip(), task_text.split(",")[1].split(":")[
            1].strip()

        task = session.query(Task).filter_by(username=username, task_name=task_name).first()

        if task:
            session.delete(task)
            session.commit()
            QMessageBox.information(self, "Information", "Task deleted successfully!")
            self.load_tasks()
        else:
            QMessageBox.warning(self, "Warning", "Task not found!")
"""

"""
def load_task(self):
    tasks = session.query(Task).all()
    self.taskList.clear()

    for task in tasks:
        item_text = f"User: {tasks.id}, Task: {tasks.title}, Task: {tasks.description}, Task: {tasks.duedate}, Task: {tasks.complated}, Task: {tasks.user_id}, Task: {tasks.categories}"
        self.listWidget_task.addItem(item_text)
"""