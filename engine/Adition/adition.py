import streamlit as st 
from database.database import *

Session = sessionmaker(bind=engine)

session = Session()

def add_register(user_id:int,entry_date:str,value:float,economy:bool):
  new_adition = Entrys(owner=user_id,value=value,entry_date=entry_date,economy=economy)
  session.add(new_adition)
  session.commit()
  return True

def load_all_entrys(user:int,economy = False):
  existing_entrys = session.query(Entrys).filter(Entrys.owner == user, Entrys.economy == economy).all()
  if existing_entrys:
    return existing_entrys
  else:
    return False
  
def menage_entry(entry_id:int,economy:bool,entry_date:str,entry_value:float,user:int=st.session_state.usuario_logado):
  existing_entry = session.query(Entrys).filter(Entrys.owner==user,Entrys.id==entry_id).first()
  if existing_entry:
    if economy != None:
      existing_entry.economy = economy
    if entry_date != None:
      existing_entry.entry_date = entry_date
    if entry_value != None:
      existing_entry.value = entry_value
    session.commit()
    return True
  else:
    return False

def delete_entry(entry_id:int,user:int=st.session_state.usuario_logado):
  existing_entry = session.query(Entrys).filter(Entrys.owner==user,Entrys.id==entry_id).first()
  if existing_entry:
    session.delete(existing_entry)
    session.commit()
    return True
  else:
    return False