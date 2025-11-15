import streamlit as st
from engine.Counts.Counts_manegement import *
from datetime import datetime
from engine.Counts.Counts_manegement import *

def load_general_Vision_per_date():
  container = st.container(border=True,key=f"Payment_container")
  select_boxes =container.container(border=False,horizontal=True)
  payment_date_selection = select_boxes.selectbox(label="Selecione um dia de vencimento",index=None,options=(list(set([item.payment_day for item in load_count(st.session_state.usuario_logado)]))))
  new_selectbox = select_boxes.selectbox("Selecione um vencimento",see_date_counts(payment_day=payment_date_selection,user=st.session_state.usuario_logado),index=None)
  total_date_payed = 0
  contas_a_serem_pagas = []
  if payment_date_selection:
    if new_selectbox:
      itens = query_counts_per_date(date=new_selectbox,user=st.session_state.usuario_logado,payment_day=payment_date_selection) 
      for i,item in enumerate(itens):
        total_date_payed += item.value
        contas_a_serem_pagas.append(item)
      new_container = container.container(border=True,)
      new_container.info(f"""

  Total de Contas no dia de vencimento: {len(itens)}

  Total a ser pago {total_date_payed}
  """)
      options_container = new_container.container(border=False,horizontal=True)
      pay = options_container.button("Pagar contas")
      if pay:
        for pagamento in contas_a_serem_pagas:
          if pay_count(pagamento.id,user_id=st.session_state.usuario_logado,date=new_selectbox):
            container.success("Conta paga com sucesso")
      infos = options_container.popover("Ver Contas por Mês")
      with infos:
        
        if new_selectbox:
          payment_day_total_value = 0
          for conta in contas_a_serem_pagas:
            payment_day_container = st.container(border=True)
            payment_day_total_value = payment_day_total_value + conta.value
            payment_day_container.info(F"""
  Descrição: {conta.description}

  Valor (Mês): R$: {conta.value}

  Número de Parcelas (Total): {conta.divisions}

""")
            options_payment_day = payment_day_container.button(label=f"Pagar Conta",key=f"pagar conta mensal {conta.id*conta.divisions+63.2}")
            if options_payment_day:
              if pay_count(conta.id,user_id=st.session_state.usuario_logado,date=new_selectbox):
                payment_day_container.success("Conta paga com sucesso")
          st.subheader(f"Total de Contas no Vencimento {new_selectbox}: {len(contas_a_serem_pagas)}")
          st.subheader(f"Total a ser pago no Vencimento {new_selectbox}: {payment_day_total_value}")

def load_count_per_payment_date(payment_date:str,user:int):
  counts = session.query(Counts).filter(Counts.payment_day==payment_date,Counts.owner==user,Counts.active==True).all()
  active_count_related = []
  for i,count in enumerate(counts):
    if count.payment_day == payment_date:
      active_count_related.append(count)
    else:
      pass
  return active_count_related

def see_date_counts(payment_day:str,user:int):
  counts = session.query(Counts).filter(Counts.payment_day==payment_day,Counts.owner==user,Counts.active==True).all()
  payed_counts = session.query(Counts_registration).filter(Counts_registration.owner==st.session_state.usuario_logado).all()
  final_dates = []
  for count in counts:
    date = load_divisions_dates(count.id)
    for item in date:
      if item not in payed_counts:
        if item in final_dates:
          pass
        else:
          final_dates.append(item)
  session.rollback()
  return final_dates
  

      
def query_counts_per_date(date:str,user:id,payment_day:str):
  counts = session.query(Counts).filter(Counts.payment_day==payment_day,Counts.owner==user,Counts.active==True).all()
  final_dates = []
  for count in counts:
    dates = load_divisions_dates(count.id)
    for item in dates:
      if item == date:
        final_dates.append(count)
      else:
        pass
  return final_dates


def load_divisions_dates(count_id:int):
    month = datetime.now().month
    year = datetime.now().year
    element= session.query(Counts).filter(Counts.id==count_id).first()
    confirmed_payments = [pay_veri.payment_confirmed_date for pay_veri in session.query(Counts_registration).filter(Counts_registration.count_id == count_id, Counts_registration.owner == st.session_state.usuario_logado).all() ]
    dates = [f"{element.payment_day}/{month}/{year}"]
    session.close()
    for i in range(int(element.divisions)):
      if month == 12:
          year = year + 1
          month = 1
          new_date = f"{element.payment_day}/{month}/{year}"
      else:
         month = month + 1
         new_date = f"{element.payment_day}/{month}/{year}"
      if new_date not in confirmed_payments:
        dates.append(new_date)
    session.rollback()
    return dates

