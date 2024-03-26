from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base,sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(50))
    password = Column(String(50))

def create_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()
def initialize_databases():
    engine = create_engine('mysql+pymysql://root:1@localhost:3306/todo_list')
    Base.metadata.create_all(engine)
    return create_session(engine)

session = initialize_databases()