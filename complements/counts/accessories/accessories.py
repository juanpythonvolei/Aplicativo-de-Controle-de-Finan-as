import streamlit as st
from engine.Counts.Counts_manegement import *
from engine.users.creation_and_update.users_creation_and_update import *
from datetime import datetime
from complements.counts.Per_date_toggle.Per_date_toggle import *

def load_delete(item:int):
        count_exclusion_password = st.text_input(label="Insira sua senha de acesso para excluir a conta",key=item.id*item.id+45.9)    
        if count_exclusion_password == search_user(query_user_by_count_owner_id(item.owner).username).password:
             count_exclusion_button = st.button(label="Exclua",key=item.id*item.id+1078.4)
             if count_exclusion_button:
                if delete_count(count_id=item.id,user_id=item.owner):
                   st.success("Conta Excluida com Sucesso")
                else:
                  st.error("Falha ao excluir a conta")

def load_infos(count_id):
  count = load_count_infos(count_id=count_id,user_id=st.session_state.usuario_logado)
  contas_pagas = load_payed_count_infos(count_id=count_id,user_id=st.session_state.usuario_logado)
  total_to_pay = count.value*count.divisions - count.value*len(contas_pagas)
  st.title(f"Conta: {count.description}")
  st.title(f"Total a ser pago: R$ {total_to_pay}")
  st.divider()
  st.subheader(f"Valor Total: R$ {count.value*count.divisions}")
  
  st.subheader(f"Total Pago: R$ {count.value*len(contas_pagas)}")
  st.divider()
  st.subheader(f"Total de parcelas pagas: {len(contas_pagas)}")

  st.subheader(f"Parcelas a serem pagas: {count.divisions-len(contas_pagas)}")
  st.divider()
  

def load_add_count():
    new_description = st.text_area("Insira a descrição da conta")
    new_Value = st.number_input("Insira o valor da conta",value=None)
    new_count_option = st.radio("Insira se a conta é ou não parcelada",["Sim","Não"])
    if new_count_option == "Sim":
      division_number = st.number_input("Insira o número de Parcelas",value=None)
    else:
       division_number = 1
    payment_day = st.text_input("Insira o dia de vencimento da Parcela")
    if new_description and new_Value and payment_day:
      confirm_count_creation = st.button("Adicionar Nova conta")
      if confirm_count_creation:
         
            if create_count(user=st.session_state.usuario_logado,value=new_Value,divisions=division_number,payment_day=str(payment_day),description=new_description):
              st.success("Conta adicionada com sucesso")

def load_settings(item:int):
        modify_description = st.text_area("Modifique a descrição da sua conta",key=item.id*item.id+67.1)
        modify_value = st.number_input("Modifique o valor da sua conta",key=item.id*item.id+17.2,value=None)
        modify_payment_day = st.text_input("Modifique a data de pagamento",key=item.id*item.id+47.4)
        modify_divisions = st.number_input("Modifique o número de parcelas",key=item.id*item.id+21.4,value=None)
        if modify_description == "":
              modify_description = None
        elif modify_divisions == "":
             modify_divisions = None
        elif modify_payment_day == "":
             modify_payment_day = None
        elif modify_value == "":
             modify_value == None
        if modify_description or modify_divisions or modify_payment_day or modify_value:
              modify_button = st.button("Modificar",key=item.id*item.id+999.1)
              if modify_button:
                if counts_modification(count_id=item.id,user_id=item.owner,payment_date=modify_payment_day,description=modify_description,value=modify_value,divisions=modify_divisions):
                    st.success("Alterações realizadas com sucesso")
                else:
                   st.error("Falha ao realizar alterações")

def load_payment(item):
    month = datetime.now().month
    year = datetime.now().year
    dates = []
    selections = st.container(horizontal=True)
    confirmed_payments = [pay_veri.payment_confirmed_date for pay_veri in session.query(Counts_registration).filter(Counts_registration.count_id == item.id, Counts_registration.owner == st.session_state.usuario_logado).all() ]
    for i in range(int(item.divisions)):
      if month == 12:
          year = year + 1
          month = 1
          new_date = f"{item.payment_day}/{month}/{year}"
      else:
         month = month + 1
         new_date = f"{item.payment_day}/{month}/{year}"
      if new_date not in confirmed_payments:
        dates.append(new_date)
    date_selection = selections.selectbox(label="Selecione uma data de pagamento",key=f"Selectbox {item.id+1,9}",options=dates,index=None)
    st.info(f"""
Valor da Parcela : R$ {item.value}
""")    
    pay=st.button(label="Pagar",key=f"Selectbox {item.id+32.1}")
    if pay:
      if pay_count(count_id=item.id,user_id=st.session_state.usuario_logado,date=date_selection):
          st.success("Conta paga com Sucesso")
      else:
         st.error("Falha ao pagar a conta")

def load_payment_history(contas,count_id):

                               
      for i,count in enumerate(contas):
          count_container = st.container(border=True)
          count_container.title(f"{i+1}º")
          count_container.info(F"""
    Valor pago: {load_count_infos(count_id=count_id,user_id=st.session_state.usuario_logado).value}

    Data do Pagamento: {count.payment_confirmed_date}

    """)
          optinons_container = st.container(border=True,horizontal=True)
          cancel_payment = optinons_container.button("Cancelar Pagamento",key=f'Cancelamento de pagamento {count.id + 8}')
          if cancel_payment:
            if delete_confirmed_payment(count_id=count_id,user_id=st.session_state.usuario_logado,date=count.payment_confirmed_date):
                st.success("Pagamento cancelado com sucesso")
            else:
              st.error("Erro ao cancelar pagamento ")
          st.divider()

      
