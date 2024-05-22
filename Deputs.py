import streamlit as st

st.title('Câmara dos Deputados')
#Fiscaliza verde, Legislativo Sustentável, Eco Política, Parlamento Ecológico, Agenda Verde


with st.sidebar:
  st.header('Melhor site de dados da camara')
  st.write('')
  st.caption('Criado por Manuela, Maju e Clarissa')

st.write('Nosso aplicativo tem como foco mostrar os dados da camara')

tab_deputado, tab_ementas, tab_projetoslei = st.tabs(['Deputados', 'Ementas', 'Projetos de Lei'])


