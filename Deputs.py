import streamlit as st

st.title('Eco Política')
#Fiscaliza verde, Legislativo Sustentável, Eco Política, Parlamento Ecológico, Agenda Verde


with st.sidebar:
  st.header('Melhor site de dados da camara')
  st.write('escrevo um texto')
  st.caption('Criado por Manuela, Maju e Clarissa')

st.write('Nosso aplicativo tem como foco mostrar os dados da camara')

tab_monitoramento, tab_ementas, tab_projetoslei = st.tabs(['Deputados', 'Ementas', 'Projetos de Lei'])

with tab_monitoramento:
  st.write('Essa aba será usada para colocar o nome dos deputados')
