import streamlit as st
from engine.Adition.adition import *
from complements.Entrys.components import *

if st.session_state.usuario_logado == None:
     st.error("Atenção, Você deve estar logado para acessar essa página")
else:
    adicao_entradas,economias = st.tabs(['Adição de Entradas', 'Economias'])
    with adicao_entradas:
        load_add_entry_tab()
    with economias:
        load_economy_tab()