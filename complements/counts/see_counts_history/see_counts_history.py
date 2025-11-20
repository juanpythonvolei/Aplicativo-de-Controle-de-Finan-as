import streamlit as st
from engine.Counts.Counts_manegement import *
from engine.users.creation_and_update.users_creation_and_update import *
from datetime import datetime
from complements.counts.Per_date_toggle.Per_date_toggle import *

def load_see_history():

  filter_container_history = st.container(border=True,horizontal=True)

  contas_pagas = session.query(Counts).filter(Counts.owner==st.session_state.usuario_logado,Counts.active==False).all()

  counts = filter_container_history.multiselect(label="Selecionar contas",options=[item.description for item in contas_pagas])

  dates = filter_container_history.date_input(label="Filtro de Data",value=None,format="DD/MM/YYYY")

  filtered_history = []

  if counts:
    for conta_paga in contas_pagas:
      if conta_paga.description in counts:
        filtered_history.append(conta_paga)
    contas_pagas = filtered_history

  if dates != None:
    for conta_paga_date in contas_pagas:
      if conta_paga_date.payment_day == dates.strftime("%d/%m/%Y"):
        filtered_history.append(conta_paga_date)
    contas_pagas = filtered_history
  
  for conta in contas_pagas:

    registros_de_contas_pagas = session.query(Counts_registration).filter(Counts_registration.count_id==conta.id,Counts_registration.owner==st.session_state.usuario_logado).all()
    container = st.container(border=True,key=f"Conta paga {conta.id*conta.value}")
    container.title(f"Conta: {conta.description}")
    container.info(f"""

Valor: R$: {conta.value}

Total de parcelas pagas: {conta.divisions}

Data de pagamento: {conta.payment_day}
""")
    ver_parcelas_pagas = container.popover("Ver parcelas pagas")
    with ver_parcelas_pagas:
     for i,registro in enumerate(registros_de_contas_pagas):
      novo_container =  st.container(border=True)
      novo_container.title(f"{registro.payment_confirmed_date}")
      conta_relacionada = load_count_infos(count_id=registro.count_id,user_id=st.session_state.usuario_logado)
      novo_container.info(f"""
Valor: {conta_relacionada.value}

Descrição: {conta_relacionada.description}

Data do Pagamento: {conta_relacionada.payment_day}""")
      restaurar_conta = novo_container.button(label="Restaurar Conta",key=f"boatao_de_restauração {i*i+5}")
      if restaurar_conta:
        if delete_confirmed_payment(count_id=registro.count_id,user_id=st.session_state.usuario_logado,date=registro.payment_confirmed_date):
           conta_restaurada = session.query(Counts).filter(Counts.id == conta.id,Counts.owner == st.session_state.usuario_logado).first()
           conta_restaurada.active = True
           session.commit()
           novo_container.success("Conta restaurada com sucesso")
        else:
          novo_container.error("erro")



