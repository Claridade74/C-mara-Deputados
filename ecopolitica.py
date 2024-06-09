import streamlit as st
import altair as alt
import pandas as pd
import random
import string
import re
import pickle
import nltk
import requests
nltk.download('stopwords')

from sklearn.feature_extraction.text import TfidfVectorizer

from nltk.corpus import stopwords
session = requests.Session()

st.set_page_config(layout="wide",
                   page_title='EcoPolítica',
                   page_icon='🌳')

st.header('EcoPolítica 🌳')
st.caption('Análise de dados abertos da Câmara dos Deputados sobre o meio ambiente')

with st.sidebar:
    st.subheader('EcoPolítica - Meio ambiente na Câmara dos Deputados')
    st.write('O presente projeto tem om a finalidade de oferecer transparência e acessibilidade às informações legislativas, o site abrange diversas questões ambientais, incluindo sustentabilidade, atividades agropecuárias, extrativismo, pesca, preservação de tribos indígenas e conservação da natureza. O principal objetivo do EcoPolítica é fornecer uma visão clara e detalhada sobre os projetos que impactam o meio ambiente.')
    st.caption('Projeto desenvolvido por Maria Julia de Oliveira, Manuela Muniz e Clarissa Treptow, sob supervisão do Prof. Matheus C. Pestana')
    st.caption('FGV ECMI')


def baixaProposicoes(ano=2024):
    arquivo = requests.get(f'http://dadosabertos.camara.leg.br/arquivos/proposicoes/xlsx/proposicoes-{ano}.xlsx')
    with open(f'proposicoes.xlsx', 'wb') as f:
        f.write(arquivo.content)
    return pd.read_excel('proposicoes.xlsx')
  
with open('modelo.pkl', 'rb') as arquivo:
  modelo = pickle.load(arquivo)

with st.spinner('Buscando base atualizada'):
   lista = []
  for i in range(2010, 2024):
      print(i)
      df = baixaProposicoes(i)
      keywords_busca = r'poluição|sucat[ae]|reciclagem|dejeto|pesca|praia|pecu[áa]ri|\bgado|descarte|queimada|lixo|meio ambiente|funai|ind.gena|garimpo|\bminera'
      df_filtrado = df[(df['codTipo'].isin([139, 291, 550, 554, 560, 561, 553, 552, 557, 632, 692, 693, 657, 658, 659, 660, 140, 390,141, 142, 136, 138])) &
                   ((df['ementa'].str.contains(keywords_busca, case=False, na=False, regex=True)) |
                    (df['keywords'].str.contains(keywords_busca, case=False, na=False, regex=True)))]
      lista.append(df_filtrado)

df_all = pd.concat(lista)
df_all = df_all[['ano', 'ementa', 'keywords']]
df_all.dropna(subset=['ementa'], inplace=True)
df_all.to_parquet('df_clarissa.parquet', index=False)

def clean_text(text):
    text = text.lower()
    text = text.replace('\n', ' ')
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

def remove_stopwords(text):
    return ' '.join([word for word in text.split() if word not in stopwords.words('portuguese')])

df_all['ementa_clean'] = df_all['ementa'].apply(clean_text)
df_all['ementa_clean'] = df_all['ementa_clean'].apply(remove_stopwords)

categoria = modelo.predict(df_all['ementa_clean'])

df_all['classificacao'] = categoria

df_all.to_parquet('df_clarissa_classificado.parquet', index=False)

obj = alt.Chart(df_all).mark_bar().encode(
    x='ano',
    y='count()',
    color='classificacao'
)

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader('Número de Projetos')
   obj = alt.Chart(df_all).mark_bar().encode(
    x='ano',
    y='count()',
    color='classificacao'
).properties(height=300)
    st.altair_chart(obj, use_container_width=True)
    
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
