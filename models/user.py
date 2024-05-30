from passlib.handlers.bcrypt import bcrypt
from sqlalchemy import Column, String, Integer, LargeBinary
from sqlalchemy.orm import relationship

from models import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(50))
    password = Column(String(50))

    # kullanıcı ile ilişki kurmak için relationship tanımlanabilir
    tasks = relationship("Task", back_populates="user")
