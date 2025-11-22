import streamlit as st
from engine.Counts.Counts_manegement import *
from engine.Adition.adition import *
from datetime import datetime
from engine.Counts.Counts_manegement import *
import pandas as pd


if st.session_state.usuario_logado == None:
     st.error("Atenção, Você deve estar logado para acessar essa página")
else:
        infos = st.container(border=True)
        infos.title("Estatísticas")
        infos.divider()
        infos.subheader("Indicadores Gerais")
        general_infos = infos.container(border=False,horizontal=True)
        filter_container = general_infos.container(border=True)
        date_filter = filter_container.date_input(label="Selecione um período",format="DD/MM/YYYY",value=None)
        infos.divider()
        valor_total_adicionado = 0
        valor_total_pago= 0
        contas_pagas= []
        contas = []
        contas_pagas_filtered = []
        contas_filtered = []
        pagamentos_filtered = []
        counts= session.query(Counts).filter(Counts.owner==st.session_state.usuario_logado).all()
        for conta in counts:
          if conta.active == False:
                if date_filter:
                    if conta.payment_day[3:5] == str(date_filter.strftime("%d/%m/%Y"))[3:5]:
                        contas_pagas_filtered.append(conta)
                contas_pagas.append(conta)
          else:
              if date_filter:
                    if conta.payment_day[3:5] == str(date_filter.strftime("%d/%m/%Y"))[3:5]:
                        contas_filtered.append(conta)
              contas.append(conta)
        pagamentos = session.query(Counts_registration).filter(Counts_registration.owner == st.session_state.usuario_logado).all()
        for pay in pagamentos:
            if date_filter:
              if pay.payment_confirmed_date[3:5] == str(date_filter.strftime("%d/%m/%Y"))[3:5]:
                  pagamentos_filtered.append(pay)
        if date_filter:
            contas = contas_filtered
            contas_pagas = contas_filtered
            pagamentos = pagamentos_filtered
       
        infos.subheader("Indicadores de Pagamentos")
        for conta in contas:
            if date_filter:
                valor_total_adicionado += conta.value
            else:
              valor_total_adicionado += conta.value * conta.divisions
        for pagamento in pagamentos:
             data = load_count_infos(count_id=pagamento.count_id,user_id=st.session_state.usuario_logado)

             valor_total_pago += data.value
             
        if len(contas) > 0 or len(contas_pagas) > 0:
          infos.info(f'Valor Total Adicionado: R${valor_total_adicionado}')
          infos.metric(label="Valor Total pago",value=f'R$: {valor_total_pago}')
          if len(pagamentos)> 0:
      
            infos.metric(label="Valor médio por pagamento",value=f"R$: {valor_total_pago/len(pagamentos)}")
          infos.metric(label="% do Valor Pago",value=valor_total_pago/valor_total_adicionado*100)
          general_infos.metric(label="Total de Contas Ativas",value=len(contas))
          if date_filter:
              general_infos.metric(label="Contas pagas do Mês",value=len(pagamentos_filtered))
          else:
            general_infos.metric(label="Total de Contas Finalizadas",value=len(contas_pagas))
          if len(contas) <= 0:
              value = 100
          else:
              if date_filter:
                  value = len(pagamentos_filtered)/len(contas_filtered)*100
              else:
                value = len(contas_pagas)/len(contas)*100
          general_infos.metric(label="% de Contas Pagas",value=value)
          infos.divider()
          infos.subheader("Indicadores de Economias")
          entradas = load_all_entrys(st.session_state.usuario_logado)
          economies = load_all_entrys(st.session_state.usuario_logado,True)
          entradas_filtered = []
          economias_filtered = []
          if date_filter:
              if entradas:
                for entrada in entradas:
                  if entrada.entry_date[3:5] == str(date_filter.strftime("%d/%m/%Y"))[3:5]:
                      entradas_filtered.append(entrada)
              if economies:
                for economy in economies:
                  if economy.entry_date[3:5] == str(date_filter.strftime("%d/%m/%Y"))[3:5]:
                      economias_filtered.append(economy)
              entradas = entradas_filtered
              economies = economias_filtered
     
          
          valor_total_em_uso = sum(valor.value for valor in entradas)
          infos.metric(label="Valor Total em uso",value=f'R$ {valor_total_em_uso-valor_total_adicionado}')

          if economies:
            infos.metric(label="Valor Total em Economia",value=f'R$ {sum(valor.value for valor in economies)}')
          infos.metric(label="% do Valor em uso gasto", value=f"{valor_total_adicionado/valor_total_em_uso * 100}")
        else:
            infos.warning("Atenção, faça mais movimentações para ter os dados exibidos")
        