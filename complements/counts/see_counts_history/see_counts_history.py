import streamlit as st
from engine.Counts.Counts_manegement import *
from engine.users.creation_and_update.users_creation_and_update import *
from datetime import datetime
from complements.counts.Per_date_toggle.Per_date_toggle import *

def load_see_history():
  contas_pagas = session.query(Counts).filter(Counts.owner==st.session_state.usuario_logado,Counts.active==False).all()
  
  for conta in contas_pagas:
    registros_de_contas_pagas = session.query(Counts_registration).filter(Counts_registration.count_id==conta.id,Counts_registration.owner==st.session_state.usuario_logado).all()
    container = st.container(border=True,key=f"Conta paga {conta.id*conta.value}")
    container.title(f"Conta: {conta.description}")
    container.info(f"""

Valor: R$: {conta.value}

Total de parcelas pagas: {conta.divisions}
""")
    ver_parcelas_pagas = container.popover("Ver parcelas pagas")
    with ver_parcelas_pagas:
     for registro in registros_de_contas_pagas:
      novo_container =  st.container(border=True)
      novo_container.title(f"{registro.payment_confirmed_date}")
      conta_relacionada = load_count_infos(count_id=registro.count_id,user_id=st.session_state.usuario_logado)
      novo_container.info(f"""
Valor: {conta_relacionada.value}

Descrição: {conta_relacionada.description}""")