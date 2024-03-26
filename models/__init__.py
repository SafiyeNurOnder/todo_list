from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.user import Baseşi

def initialize_databases():
    engine = create_engine('mysql+pymysql://root:1@localhost:3306/todo_list')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return engine, session