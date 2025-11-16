import streamlit as st
from engine.Counts.Counts_manegement import *
from datetime import datetime
from engine.Counts.Counts_manegement import *
import pandas as pd


if st.session_state.usuario_logado == None:
     st.error("Atenção, Você deve estar logado para acessar essa página")
else:
        
        contas = session.query(Counts).filter(Counts.active==True,Counts.owner==st.session_state.usuario_logado).all()
        contas_pagas =  session.query(Counts).filter(Counts.active==False,Counts.owner==st.session_state.usuario_logado).all()
        if len(contas) > 0 and len(contas_pagas) > 0:
          pagamentos_realizados = session.query(Counts_registration).filter(Counts.owner==st.session_state.usuario_logado).all()
          dict_ = {}
          lista = []
          data_frames = []
          for conta in contas:
            dados = {
              'Valor': [f"{conta.value}"],
              'Descrição': [f"{conta.description}"],
              'Data de Pagamento': [f"{conta.payment_day}"],
            
          }
          data_frames.append(pd.DataFrame(dados))
          st.metric(label="% de Contas Pagas",value=len(contas_pagas)/len(contas)*100)
        else:
            st.warning("Atenção, faça mais movimentações para ter os dados exibidos")