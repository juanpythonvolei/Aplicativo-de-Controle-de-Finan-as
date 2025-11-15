import streamlit as st
from engine.users.creation_and_update.users_creation_and_update import create_user

def load_create_user_page():

  user_creation_container = st.container(
    border=True
  )

  user_creation_container.title("Crie aqui seu novo usuário")

  new_user_login = user_creation_container.text_input("Insira aqui seu novo usuário")
  new_user_keyword = user_creation_container.text_input("Insira aqui sua nova senha",type="password")

  create_new_user_buttons = user_creation_container.container(
    border=True,
    horizontal=True
  )

  create_new_user_button = create_new_user_buttons.button("Criar novo Usuário")


  if create_new_user_button:
    if new_user_login and new_user_keyword:
      if create_user(user=new_user_login,password=new_user_keyword):
        st.success("Usuário criado com sucesso")
      else:
        st.error("Erro ao criar seu usuário")
    elif not new_user_login:
      st.error("Preecha o campo de novo usuário")
    else:
      st.error("Preenhca o campo de nova senha")