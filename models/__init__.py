from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#import os

#ip=os.environ["IP"]

# MySQL veritabanı bağlantısı oluşturma
#engine = create_engine('mysql+pymysql://root:1@'+ip+':3306/todoList')
engine = create_engine('mysql+pymysql://root:1@localhost:3306/todo_list')
Base = declarative_base()

# Oturum oluşturma
Session = sessionmaker(bind=engine)
session = Session()

# Tablo tanımlamaları
from models import user, task

Base.metadata.create_all(engine)  # Model sınıflarını kullanarak veritabanı ve tabloları oluşturuyoruz.
