import streamlit as st
from Início import *
from complements.counts.Visualização_Geral_das_Contas import *



if "usuario_logado" not in st.session_state:
      st.session_state.usuario_logado = None
      st.switch_page("Início.py")
else:
      if st.session_state.usuario_logado == None:
            st.error("Você deve estar logado para acessar o aplicativo")
      else:
            load_general_vision()