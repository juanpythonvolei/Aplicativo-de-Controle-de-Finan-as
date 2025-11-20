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
        filters_container = general_vision_contanier.container(border=False,horizontal=True)
        date_based_vision = subcontainer.toggle("Visualizar por data de vencimento")
        count_based_vision = subcontainer.toggle("Visualizar Contas Finalizadas")
        if count_based_vision and not date_based_vision:
          load_see_history()
        if date_based_vision and not count_based_vision:
          load_general_Vision_per_date()
        if not date_based_vision and not count_based_vision:
          counts = load_count(user=st.session_state.usuario_logado)
          filter_selection = filters_container.multiselect(label="Selecione as contas que deseja visualizar",options=[conta.description for conta in counts])
          date_filter = filters_container.date_input(label="Filtro de Data",value=None,format="DD/MM/YYYY")
          filtereds = []
          if filter_selection:
            for count_to_filter in counts:
              if count_to_filter.description in filter_selection:
                      filtereds.append(count_to_filter)
            counts = filtereds
          if date_filter != None:
            for date_filtered_count in counts:
                if date_filtered_count.payment_day == date_filter.strftime("%d/%m/%Y"):
                  filtereds.append(date_filtered_count)
            counts = filtereds
          general_vision_contanier.divider()
          
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
     
 
