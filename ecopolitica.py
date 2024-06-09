import streamlit as st
import altair as alt
import pandas as pd
import random

st.set_page_config(layout="wide",
                   page_title='EcoPolítica',
                   page_icon='🌳')

st.header('EcoPolítica')
st.caption('Análise de dados abertos da Câmara dos Deputados sobre o meio ambiente')

with st.sidebar:
    st.subheader('EcoPolítica - Meio ambiente na Câmara dos Deputados')
    st.write('O presente projeto tem om a finalidade de oferecer transparência e acessibilidade às informações legislativas, o site abrange diversas questões ambientais, incluindo sustentabilidade, atividades agropecuárias, extrativismo, pesca, preservação de tribos indígenas e conservação da natureza. O principal objetivo do EcoPolítica é fornecer uma visão clara e detalhada sobre os projetos que impactam o meio ambiente.')
    st.caption('Projeto desenvolvido por Maria Julia de Oliveira, Manuela Muniz e Clarissa Treptow, sob supervisão do Prof. Matheus C. Pestana')
    st.caption('FGV ECMI')
numeros_aleatorios = [random.randint(10, 100) for _ in range(6)]

dados_fakes = pd.DataFrame({
    'Ano': [2019, 2020, 2021, 2022, 2023, 2024],
    'Número de Projetos': [10, 20, 30, 40, 50, 60],
    'Projetos Contra': [9, 12, 18, 25, 15, 10]
})
dados_fakes['Número de Projetos'] = dados_fakes['Número de Projetos'] + numeros_aleatorios
dados_fakes['Projetos Contra'] = dados_fakes['Projetos Contra'] + numeros_aleatorios
dados_fakes['Projetos A Favor'] = dados_fakes['Número de Projetos'] - dados_fakes['Projetos Contra'] - [random.randint(1, 5) for _ in range(6)]


dados_deputados = pd.DataFrame({
    'Deputado': ['João', 'Maria', 'José', 'Ana', 'Pedro'],
    'Partido': ['A', 'B', 'A', 'C', 'A'],
    'Projetos A Favor': [10, 20, 30, 40, 50],
    'Projetos Contra': [5, 10, 15, 20, 25]
})
dados_deputados['Projetos A Favor'] = dados_deputados['Projetos A Favor'] + numeros_aleatorios[:5]
dados_deputados['Projetos'] = dados_deputados['Projetos A Favor'] + dados_deputados['Projetos Contra']


col1, col2, col3 = st.columns(3)

with col1:
    st.subheader('Número de Projetos')
    grafico_projetos = alt.Chart(dados_fakes).mark_bar().encode(x='Ano:N', y='Número de Projetos:Q').properties(height=300)
    st.altair_chart(grafico_projetos, use_container_width=True)
    st.subheader('Frentes Parlamentares')
    dados_frentes = pd.DataFrame({
        'Frente Parlamentar': ['Frente A', 'Frente B', 'Frente C'],
        'Número de Projetos': [10, 20, 30],
        'Número de Deputados': [5, 10, 15]
    })
    dados_frentes['Número de Projetos'] = dados_frentes['Número de Projetos'] + numeros_aleatorios[3:]
    graf_frentes = alt.Chart(dados_frentes).mark_bar().encode(y='Frente Parlamentar:N',
                                                              x='Número de Projetos:Q').properties(height=250)
    st.altair_chart(graf_frentes, use_container_width=True)
    st.dataframe(dados_frentes)

with col2:
    st.subheader('Projetos A Favor e Contra')
    grafico_projetos_a_favor = alt.Chart(dados_fakes).mark_line(color='cornflowerblue').encode(x='Ano:N', y='Projetos A Favor:Q').properties(height=300)
    grafico_projetos_contra = alt.Chart(dados_fakes).mark_line(color='red').encode(x='Ano:N', y='Projetos Contra:Q').properties(height=300)
    st.altair_chart(grafico_projetos_a_favor, use_container_width=True)
    st.altair_chart(grafico_projetos_contra, use_container_width=True)

with col3:
    st.subheader('Deputados')
    st.dataframe(dados_deputados)
    st.subheader('Projetos por partido')
    df_group_party = dados_deputados.groupby('Partido')['Projetos'].sum().reset_index()
    grafico_por_partido = alt.Chart(df_group_party).mark_bar(color='orchid').encode(x='Partido:N', y='Projetos:Q').properties(height=300)
    st.altair_chart(grafico_por_partido, use_container_width=True)
