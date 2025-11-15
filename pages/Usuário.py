import streamlit as st
from complements.login.Alteração_de_Senha_e_username import load_password_chage
from complements.login.Criação_de_Usuário import load_create_user_page


options = st.sidebar.selectbox(
  "Selecione uma opção",
  ["Criar Usuário", "Alterar Senha ou username"],
  index=None,
  placeholder="Selecione uma opção"

  
)

if options:
  if options == "Criar Usuário":
    load_create_user_page()
  elif options == "Alterar Senha ou username":
    load_password_chage()
else:
  st.title("Gerencimento de Usuário")
  st.subheader("Selecione, na aba de menu, o Ajuste desejado")


