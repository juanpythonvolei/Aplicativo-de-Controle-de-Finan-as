import streamlit as st 
from engine.users.creation_and_update import *
from engine.users.Acess.user_acess import *
from engine.Counts.Counts_manegement import query_user_by_count_owner_id

if "usuario_logado" not in st.session_state:
      st.session_state.usuario_logado = None

if st.session_state.usuario_logado == None:

  main_container = st.container(
    border=True
  )
  main_container.title("Aplicativo de Controle de Finanças")
  created_user_login = main_container.text_input("Insira seu usuário")
  created_user_keyword = main_container.text_input("Insira sua senha",type="password")
  acess_container = main_container.container(
    border=True,
    horizontal=True
  )
  acess_button = acess_container.button("Acessar")

  if acess_button:
    if created_user_login and created_user_keyword:
      login = acess_user(user=created_user_login,password=created_user_keyword)
      if login:
        st.success(f"Acesso realizado com sucesso")
      else:
        st.error("Usuário ou senha incorretos")
    elif not created_user_login:
      st.error("Preeehca o campo de usuário")
    else:
      st.error("Preencha o campo de senha")

else:
  finalize_section = st.container(border=True)
  finalize_section.title(f"{query_user_by_count_owner_id(st.session_state.usuario_logado).username}")
  finalize_section.button("Finalizar Sessão")
  if finalize_section:
    st.session_state.usuario_logado = None