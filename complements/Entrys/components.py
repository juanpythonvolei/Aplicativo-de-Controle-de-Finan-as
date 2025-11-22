from engine.Adition.adition import *

def load_add_entry_tab():
  container_entradas = st.container(border=True)
  container_entradas.title("Adicione e visualize aqui seus valores")
  componentes = container_entradas.container(border=False,horizontal=True)
  container_adicao = componentes.container(border=True)
  container_historico_entradas = componentes.container(border=True)
  entry_value = container_adicao.number_input(label="Valor do Depósito",value=None)
  entry_date = container_adicao.date_input(label="Data do Depósito",format="DD/MM/YYYY")
  if_economy = None
  economy = container_adicao.pills(label="Economia",options=['Sim','Não'])
 
  if economy == 'Sim':
    if_economy = True

    
  else:
    if_economy = False

  make_entry = container_adicao.button("Depositar")
  if make_entry:
  
    if entry_date and entry_value and economy:
      if add_register(user_id=st.session_state.usuario_logado,entry_date=entry_date.strftime("%d/%m/%Y"),value=entry_value,economy=if_economy):
        container_adicao.success("Depósito realizado com sucesso")
      else:
        container_adicao.error("Erro ao Depositar")
    else:
      container_adicao.warning("Ainda há campos que não foram devidamente preenchidos")
  date_filter = container_historico_entradas.date_input(label="Selecione um período",value=None,format="DD/MM/YYYY")
  entradas = load_all_entrys(user=st.session_state.usuario_logado)
  lista = []
  if entradas:
    if date_filter:
      for date in entradas:
        if date.entry_date[3:5] == str(date_filter.strftime("%d/%m/%Y"))[3:5]:
          lista.append(date)
      entradas  = lista
    valor_total_em_uso=0
    for i,item in enumerate(entradas):
      valor_total_em_uso += item.value
      container_entrada_existente = container_historico_entradas.container()
      container_entrada_existente.info(F"""
  Valor da Entrada: {item.value}

  Data da Entrada: {item.entry_date}""")
      container_opcoes = container_entrada_existente.container(border=False,horizontal=True)
      botao_alterar_entrada = container_opcoes.popover("Modificar")
      with botao_alterar_entrada:
        modified_entry_value = st.number_input(label="Modifique o valor da entrada",key=f"change_valuef: {item.id*3.1245}",value=None)
        modifed_entry_date = st.date_input(label="Modifique a data do Depósito",format="DD/MM/YYYY",key=f"change_Date {item.id*0.147}",value=None)
        modified_entry_economy = st.pills(label="Modifique se é Economia ou não",key=f"change_economy {item.id*7.456}",options=['Sim','Não'])
        modify_button = st.button("Modificar",f"change_button {item.id*12.5633}")
        if modify_button:
          if modified_entry_economy or modifed_entry_date or modified_entry_value:
            if modified_entry_economy:
              modified_economy_value = None
              if modified_entry_economy == 'Sim':
                  modified_economy_value = True
              else:
                modified_economy_value = False
            else:
              modified_economy_value = None
            date = None
            if modifed_entry_date:
              date = modifed_entry_date.strftime("%d/%m/%Y")
            else:
              date = None
            if menage_entry(item.id,economy=modified_economy_value,entry_date=date,entry_value=modified_entry_value):
              st.success("Sucesso ao alterar a Entrada")
            else:
              st.error("Erro ao alterar a entrada")
          else:
            st.warning("Modifique, ao menos, 1 campo para realizar alterações")            

      botao_excluir_entrada = container_opcoes.button("Exluir",f"{i*9+1}")
      if botao_excluir_entrada:
        if delete_entry(item.id):
          container_historico_entradas.success("Entrada excluida com sucesso")
      container_entrada_existente.divider()
    to_count = []
    counts = session.query(Counts).filter(Counts.owner == st.session_state.usuario_logado).all()
    if date_filter:
      for count in counts:
        if count.payment_day[3:5] == str(date_filter.strftime("%d/%m/%Y"))[3:5]:
          to_count.append(count)
      to_discount = sum(elemento.value for elemento in to_count)
    else:
      to_count = counts
      to_discount = sum(elemento.value * elemento.divisions for elemento in to_count)
    container_historico_entradas.subheader(f"Valor Total em uso restante: R$ {valor_total_em_uso-to_discount}")
  else:
    container_historico_entradas.warning("Atenção, você não possúi entradas registradas para uso contínuo")


def load_economy_tab():
  economias = session.query(Entrys).filter(Entrys.owner == st.session_state.usuario_logado, Entrys.economy == True).all()
  total_economizado = 0
  if len(economias)> 0 :
    container = st.container(border=True)
    container.title(f"Total em economia: R$ {sum(conta.value for conta in economias)}")
    container.divider()
    container.subheader("Suas Economias")
    for item in economias:
      total_economizado += item.value
      economy_container = container.container(border=True)
      economy_container.info(F"""
      Valor da Entrada de Economia: {item.value}

      Data da Entrada como Economia: {item.entry_date}
  """)
      options_container = economy_container.container(border=False,horizontal=True)
      modify_button = options_container.popover("Modificar")
      with modify_button:
        modify_economy_value = st.number_input(label="Modifique o valor dessa economia",value=None,key=f"economy_change: {item.id*12*item.value}")
        modify_economy_date = st.date_input(label="Modifique a data dessa economia",value=None,format="DD/MM/YYYY",key=f"change_economy_date {item.id*0.489}")
        if_modify_economy = st.pills(label="Modifique se é Economia ou não",key=f"change_economy_if {item.id*963}",options=['Sim','Não'])
        if modify_economy_date or modify_economy_value or if_modify_economy:
          modify_economy_button = st.button("Modificar",f"modify_button {item.id*789}")
          if modify_economy_button:
            modified_economy_value = None
            if if_modify_economy == 'Sim':
                    modified_economy_value = True
            else:
                  modified_economy_value = False
            date = None
            if modify_economy_date:
                date = modify_economy_date.strftime("%d/%m/%Y")
            else:
                date = None
            if menage_entry(entry_id=item.id,economy=modified_economy_value,entry_date=date,entry_value=modify_economy_value):
              st.success("Entrada Modificada com sucesso")
  else:
    st.warning("Atenção, Você não possui nenhuma economia")
  