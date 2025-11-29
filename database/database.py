import sqlalchemy as sq
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String,Float,Boolean
import streamlit as st



engine = create_engine(url=st.secrets['database_key'],echo=False)
base = declarative_base()

class Users(base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True,autoincrement=True,unique=True)
    username = Column(String,unique=True,nullable=False)
    password = Column(String,nullable=False)

class Counts(base):
    __tablename__ = "Contas"
    id = Column(Integer,primary_key=True,autoincrement=True,unique=True)
    owner = Column(Integer)
    value = Column(Float)
    divisions = Column(Float)
    payment_day = Column(String)
    description = Column(String)
    active = Column(Boolean)

class Counts_registration(base):
    __tablename__ = "Registro de Pagamentos"
    id = Column(Integer,primary_key=True,autoincrement=True,unique=True)
    owner = Column(Integer)
    count_id = Column(Integer)
    payment = Column(Boolean)
    payment_confirmed_date = Column(String)

class Entrys(base):
    __tablename__ = "Entradas"
    id = Column(Integer,primary_key=True,autoincrement=True,unique=True)
    owner = Column(Integer)
    value = Column(Float)
    entry_date = Column(String)
    economy = Column(String)

    
base.metadata.create_all(engine)