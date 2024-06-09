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
  
with st.spinner('Buscando base atualizada'):
  df = baixaProposicoes(2024)
  keywords_busca = r'poluição|sucat[ae]|reciclagem|dejeto|pesca|praia|pecu[áa]ri|\bgado|descarte|queimada|lixo|meio ambiente|funai|ind.gena|garimpo|\bminera'
  df_filtrado = df[(df['codTipo'].isin([139, 291, 550, 554, 560, 561, 553, 552, 557, 632, 692, 693, 657, 658, 659, 660, 140, 390,141, 142, 136, 138])) &
   ((df['ementa'].str.contains(keywords_busca, case=False, na=False, regex=True)) |
   (df['keywords'].str.contains(keywords_busca, case=False, na=False, regex=True)))]
  
with open('modelo.pkl', 'rb') as arquivo:
  modelo = pickle.load(arquivo)
  
def clean_text(text):
    text = text.lower()
    text = text.replace('\n', ' ')
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text
  
def remove_stopwords(text):
    return ' '.join([word for word in text.split() if word not in stopwords.words('portuguese')])

df_all = pd.read_parquet('df_clarissa_classificado.parquet')

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader('Número de Projetos')
    obj = alt.Chart(df_all).mark_bar().encode(
        x='ano',
        y='count()',
        color='classificacao'
    )
    st.altair_chart(obj, use_container_width=True)
    st.metric('Nº de projetos em 2024:', len(df_filtrado))
  
with col2:
    st.subheader('Projetos A Favor e Contra')
    grafico_projetos_a_favor = alt.Chart(df_all).mark_line(color='cornflowerblue').encode(x='Ano:N', y='Projetos A Favor:Q').properties(height=300)
    grafico_projetos_contra = alt.Chart(df_all).mark_line(color='red').encode(x='Ano:N', y='Projetos Contra:Q').properties(height=300)
    st.altair_chart(grafico_projetos_a_favor, use_container_width=True)
    st.altair_chart(grafico_projetos_contra, use_container_width=True)
