from sqlalchemy.orm import sessionmaker
from database.database import Users,engine
import streamlit as st

Session = sessionmaker(bind=engine)

session = Session()



def acess_user(user:str,password:str):
  user_found = session.query(Users).filter(Users.username==user,Users.password==password).first()
  if user_found:
    st.session_state.usuario_logado = user_found.id
    return st.switch_page("pages/Home.py")
  else:
    return False