from functools import wraps
from sqlalchemy import (Column, Integer, create_engine, Text)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError, StatementError

DB_URL = "mysql://<username>:<password>@<host>:<port>/<schema>"

Base = declarative_base()
engine = create_engine(DB_URL, pool_recycle=3600, connect_args={'connect_timeout': 60})
session = sessionmaker(bind=engine)


#Create a table in MySQL with name: Users and columns: idusers, username, email, password
class Users(Base):
	__tablename__ = 'users'
	idusers = Column(Integer, primary_key=True)
	username = Column(Text)
	email = Column(Text)
	password=Column(Text)
