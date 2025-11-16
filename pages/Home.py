import streamlit as st
from Início import *
from complements.counts.Visualização_Geral_das_Contas import *


print(st.session_state)

if st.session_state.usuario_logado == None:
  st.error("Atenção, você deve estar logado para acessar essa página")
else:
  load_general_vision()