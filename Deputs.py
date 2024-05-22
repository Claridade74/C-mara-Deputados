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

placeholder = st.empty()

# Replace the placeholder with some text:
placeholder.text("Hello")

# Replace the text with a chart:
placeholder.line_chart({"data": [1, 5, 2, 6]})

# Replace the chart with several elements:
with placeholder.container():
    st.write("This is one element")
    st.write("This is another")

# Clear all those elements:
placeholder.empty()
