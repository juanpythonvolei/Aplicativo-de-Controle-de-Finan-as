import streamlit as st
from engine.Counts.Counts_manegement import *
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
        valor_total_adicionado = 0
        valor_total_pago= 0
        contas_pagas= []
        contas = []
        filtradas_pagas = []
        filtradas_ativas = []
        counts= session.query(Counts).filter(Counts.owner==st.session_state.usuario_logado).all()
        for conta in counts:
          if conta.active == False:
                contas_pagas.append(conta)
          else:
              contas.append(conta)
        pagamentos = session.query(Counts_registration).filter(Counts_registration.owner == st.session_state.usuario_logado).all()
        general_infos = infos.container(border=False,horizontal=True)
        infos.divider()
        infos.subheader("Inficadores de Pagamentos")
        for conta in contas:
            valor_total_adicionado += conta.value * conta.divisions
        for pagamento in pagamentos:
             valor_total_pago += load_count_infos(pagamento.count_id,user_id=st.session_state.usuario_logado).value
       
        if len(contas) > 0 or len(contas_pagas):
          infos.info(f'Valor Total Adicionado: R${valor_total_adicionado}')
        
          infos.metric(label="Valor Total pago",value=f'R$: {valor_total_pago}')
          if len(pagamentos)> 0:
      
            infos.metric(label="Valor médio por pagamento",value=f"R$: {valor_total_pago/len(pagamentos)}")
            
          general_infos.metric(label="Total de Contas Ativas",value=len(contas))
          
          general_infos.metric(label="Total de Contas Finalizadas",value=len(contas_pagas))
          if len(contas) <= 0:
              value = 100
          else:
              value = len(contas_pagas)/len(contas)*100
          general_infos.metric(label="% de Contas Pagas",value=value)
        else:
            infos.warning("Atenção, faça mais movimentações para ter os dados exibidos")
        