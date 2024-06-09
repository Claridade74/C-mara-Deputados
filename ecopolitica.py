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
df_all.rename(columns={'classificacao': 'Classificação'}, inplace=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader('Número de Projetos')
    obj = alt.Chart(df_all).mark_bar().encode(
        x=alt.X('ano', title='Ano'),
        y=alt.Y('count()', title='Número de Projetos')
    ).properties(height=300)
    st.altair_chart(obj, use_container_width=True)
    st.metric('Nº de projetos em 2024:', len(df_filtrado))
  
with col2:
    st.subheader('Projetos A Favor e Contra')
    grafico_projetos = alt.Chart(df_all).mark_line().encode(
        x=alt.X('ano', title='Ano') ,
        y=alt.Y('count()', title='Número de Projetos'),
        color=alt.Color('Classificação').legend(title='Classificação', orient='bottom')
    ).properties(height=360)    
    st.altair_chart(grafico_projetos, use_container_width=True)


st.subheader('Últimos projetos')
st.write('Abaixo, você encontra os últimos projetos iniciados que são relacionados ao meio ambiente.')
st.dataframe(df_filtrado[['siglaTipo', 'numero', 'ano', 'ementa']].tail(10), use_container_width=True)


st.subheader('Frentes relacionadas ao Meio Ambiente')
st.write('Abaixo, você encontra as frentes parlamentares relacionadas ao meio ambiente, bem como seus coordenadores e contato.')
with st.spinner('Baixando dados das frentes...'):
    url_base = 'https://dadosabertos.camara.leg.br/api/v2/frentes?idLegislatura=57'
    content = session.get(url_base).json()
    frentes = []
    for item in content['dados']:
        frentes.append(item)
    while content['links'][1]['rel'] == 'next':
        print(content['links'][1]['href'])
        url = content['links'][1]['href']
        content = session.get(url).json()
        for item in content['dados']:
            frentes.append(item)
    df_frentes = pd.DataFrame(frentes)
    df_frentes = df_frentes[df_frentes['titulo'].str.contains('agro|ambiente|lixo|rural|amaz.nia|verde|ecolog|campo|nutricional|bambu', na=False, regex=True, case=False)]
    for i, row in df_frentes.iterrows():
        frente_info = session.get(row['uri']).json()
        coordenador = frente_info['dados']['coordenador']
        with st.container(border=True):
            subcol1, subcol2 = st.columns([1, 7])
            subcol1.image(coordenador['urlFoto'], width=100)
            subcol2.subheader(row['titulo'])
            subcol2.write(f'Coordenador: {coordenador["nome"]} - {coordenador["siglaPartido"]}-{coordenador["siglaUf"]}')
            subcol2.caption(f'Contato: {coordenador["email"]}')
        subcol2.write(f'Coordenador: {coordenador["nome"]} - {coordenador["siglaPartido"]}-{coordenador["siglaUf"]}')
        subcol2.caption(f'Contato: {coordenador["email"]}')
