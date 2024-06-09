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
   
df_all = pd.concat(lista)
df_all = df_all[['ano', 'ementa', 'keywords']]
df_all.dropna(subset=['ementa'], inplace=True)

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
