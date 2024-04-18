from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from models import Base


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    description = Column(String(255))
    due_date = Column(DateTime)
    priority = Column(Integer)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    categories = Column(String(255))

    # kullanıcı ile ilişki kurmak için relationship tanımlanabilir
    user = relationship("User", back_populates="tasks")
