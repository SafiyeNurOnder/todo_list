from models.task import Task


class TodoList:
    def __init__(self, session):
        self.session = session

    def add_task(self, title, description=''):
        new_task = Task(title=title, description=description)
        self.session.add(new_task)
        self.session.commit()

    def get_all_tasks(self):
        return self.session.query(Task).all()

    def get_task_by_id(self,task_id):
        return self.session.query(Task).filter_by(id=task_id).first()

    def update_task(self, task_id, title=None, description=None, due_date=None, priority=None, completed=None, user_id=None):
        task = self.get_task_by_id(task_id)
        if task:
            if title:
                task.title = title
            if description:
                task.description = description
            if due_date is not None:
                task.due_date = due_date
            if priority is not None:
                task.priority = priority
            if completed is not None:
                task.completed = completed
            if user_id is not None:
                task.user_id = user_id
            self.session.commit()

    def delete_task(self, task_id):
        task = self.get_task_by_id(task_id)
        if task:
            self.session.delete(task)
            self.session.commit()