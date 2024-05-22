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
  col1, col2, col3 = st.columns(3)

with col1:
   st.header("A cat")
   st.image("https://static.streamlit.io/examples/cat.jpg")

with col2:
   st.header("A dog")
   st.image("https://static.streamlit.io/examples/dog.jpg")

with col3:
   st.header("An owl")
   st.image("https://static.streamlit.io/examples/owl.jpg")

