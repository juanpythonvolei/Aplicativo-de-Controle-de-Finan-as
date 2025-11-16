from complements.counts.accessories.accessories import *
from complements.counts.see_counts_history.see_counts_history import *

def load_general_vision():
  general_vision_contanier = st.container(border=True)
  title_container = general_vision_contanier.container(horizontal=True)
  title_container.title("Visão Geral das Contas")
  add_new_count =title_container.popover("➕")
  with add_new_count:
          load_add_count()
  try:
      general_vision_contanier.divider()
      subcontainer = general_vision_contanier.container(border=False,horizontal=True,horizontal_alignment="distribute",vertical_alignment="center")
      counts = load_count(user=st.session_state.usuario_logado)
      date_based_vision = subcontainer.toggle("Visualizar por data de vencimento")
      count_based_vision = subcontainer.toggle("Visualizar Contas Finalizadas")
      if date_based_vision and not count_based_vision:
        load_general_Vision_per_date()
      if count_based_vision and not date_based_vision:
        load_see_history()
      general_vision_contanier.divider()
      if not date_based_vision and not count_based_vision:
        
        try:
          for item in counts:
              item_container = st.container(border=True,horizontal=True,key=item.id*item.id**item.id*12.3,vertical_alignment="center")
              name_container = item_container.container(border=False,key=f"{item.id*99.12}")
              name_container.subheader(f"{item.description}")
              name_container.info(f"""
              Valor da Conta (Mês) : R$ {item.value}

              Quantidade de Parcelas: {item.divisions}

              Data de Vencimento (Todo dia) : {item.payment_day}

        """)
              options_container = item_container.container(border=False,horizontal=True,key=item.id*item.id**item.id*12.4)
              settings_count_button = options_container.popover("⚙️")
              with settings_count_button:
                load_settings(item=item)
              delete_count_button = options_container.popover("🗑️")
              with delete_count_button:
                load_delete(item=item)
              pay_count_button = options_container.popover("💵")
              with pay_count_button:
                load_payment(item=item)
              contas = load_payed_count_infos(count_id=item.id,user_id=st.session_state.usuario_logado)
              if contas:
                history_count_payed_button = options_container.popover("📑")
                with history_count_payed_button:
                  load_payment_history(count_id=item.id,contas=contas)
                info_count_button = options_container.popover("🔎")
                with info_count_button:
                  load_infos(item.id)
        except:
          pass
  except:
    st.warning("Atenção Crie uma conta para Iniciar")
