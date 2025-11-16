import streamlit as st
from engine.users.creation_and_update.users_creation_and_update import *

def load_password_chage():

  password_change_container = st.container(
    border=True
  )

  password_change_container.title("Altere seu usuário/Resgate ou altere aqui sua senha")
  user_created_login_validation = password_change_container.text_input("Insira aqui seu usuário existente")
  if user_created_login_validation:
    user_created_id = search_user(username=user_created_login_validation)
    if user_created_id:
      with password_change_container.popover("🗑️"):
            deletion_password = st.text_input(type='password',label="Insira sua senha atual para excluir seu usuário")
            if deletion_password == user_created_id.password:
              delete_created_user = st.button("Excluir Usuário")
              if delete_created_user:
                if delete_user(user_id=user_created_id.id):
                  password_change_container.success("Usuário Excluido com Sucesso")
                else:
                  password_change_container.error("Erro ao excluir usuário")
            else:
              password_change_container.error("Senhas não conferem")
      new_password_input = password_change_container.text_input("Insira aqui sua nova senha",type="password")
      new_user_name_input = password_change_container.text_input("Insira aqui seu novo username")
      if new_password_input or new_user_name_input:
        change_password_buttons = password_change_container.container(
        border=True,
        horizontal=True 
      )
        modified_password_button = change_password_buttons.button("Alterar")
       
        if modified_password_button:
          if new_user_name_input == "":
              new_user_name_input = None
          if new_password_input == "":
            new_password_input = None
          if update_user_password_username(user=user_created_id.id,new_password=new_password_input,new_username=new_user_name_input):
            password_change_container.success("Senha alterada com sucesso")
          else:
            password_change_container.error("Ocorreu um erro, tente novamente")
        
    else:
        password_change_container.error("Usuário não encontrado. Insira um usuário válido")
  else:
      password_change_container.warning("Atenção: Você deve inserir um usuário existente para alterar a senha")





