# Imports gerais
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from st_aggrid import AgGrid

# Imports específicos
from reuse import dict_partes_questionario


def obter_dataframe_respostas_multiplas(
        df: pd.DataFrame,
        resposta_multipla: dict,
        idx_pergunta: int,
        textos_alternativo: list,
        qtde_perc: str) -> pd.DataFrame:
    """
    Obtém um dataframe com as respostas de uma pergunta de multipla escolha.

    Parâmetros:
    -----------
    df:pd.DataFrame
        Dataframe com as respostas do questionário.
    resposta_multipla:dict
        Dicionário com as respostas de uma pergunta de multipla escolha.
    idx_pergunta:int
        Índice da pergunta de multipla escolha.
    textos_alternativo:list
        Lista de textos alternativos para as perguntas.
    qtde_perc:str
        Quantidade ou percentual a ser apresentado.


    Retornos:
    ----------
    sub:pd.DataFrame
        Dataframe com as respostas de uma pergunta de multipla escolha.
    """

    # Obtém as respostas da pergunta de multipla escolha (e realiza a soma)
    sub = df[df.columns[resposta_multipla[idx_pergunta]]].sum(
        axis=0).to_frame()

    # Converte para percentual se necessário
    if qtde_perc == 'Percentual':
        limit = df[df.columns[resposta_multipla[idx_pergunta]]
                   ].dropna().shape[0]
        sub = np.round((sub / limit) * 100, 2)

    sub = sub.reset_index()

    # Adiciona o texto alternativo da pergunta
    sub['texto_alternativo'] = textos_alternativo[resposta_multipla[idx_pergunta]
                                                  [0]:resposta_multipla[idx_pergunta][-1]+1]

    # Converte para percentual se necessário
    if qtde_perc == 'Percentual':
        sub.rename(columns={
                   0: 'Percentual (%)', 'texto_alternativo': textos_alternativo[idx_pergunta]}, inplace=True)
    else:
        sub = sub.rename(
            columns={0: "Quantidade", 'texto_alternativo': textos_alternativo[idx_pergunta]})

    # Seleciona as colunas de interesse
    sub = sub[[sub.columns[2], sub.columns[1]]]
    return sub


def obter_dataframe_resposta_unica(
        df: pd.DataFrame,
        idx_pergunta: int,
        texto_alternativo: list,
        qtde_perc: str) -> pd.DataFrame:
    """
    Obtém um dataframe com as respostas de uma pergunta de unica escolha.

    Parâmetros:
    -----------
    df:pd.DataFrame
        Dataframe com as respostas do questionário.
    idx_pergunta:int    
        Índice da pergunta de unica escolha.
    texto_alternativo:list  
        Lista de textos alternativos para as perguntas.
    qtde_perc:str   
        Quantidade ou percentual a ser apresentado.

    Retornos:
    ----------
    sub:pd.DataFrame
        Dataframe com as respostas de uma pergunta de unica escolha.
    """

    # Obtém as respostas da pergunta de unica escolha (e realiza a contagem)
    sub = df[[df.columns[idx_pergunta]]]
    # Coluna fantasma para contar as respostas
    sub['c'] = 1
    sub_agg = sub.groupby(sub.columns[0]).agg('count')[['c']]

    # Converte para percentual se necessário
    if qtde_perc == "Percentual":
        sub_agg = np.round((sub_agg / sub.shape[0]) * 100, 2)

    # Realiza a ordenação pela quantidade de respostas
    sub_agg = sub_agg.reset_index()
    sub_agg = sub_agg.sort_values(['c'], ascending=False, ignore_index=True)

    # Converte para percentual se necessário
    if qtde_perc == "Quantidade":
        sub_agg.rename(columns={
                       'c': 'Quantidade', sub.columns[0]: texto_alternativo[idx_pergunta]}, inplace=True)
    else:
        sub_agg.rename(columns={
                       'c': 'Percentual (%)', sub.columns[0]: texto_alternativo[idx_pergunta]}, inplace=True)

    return sub_agg


def obter_grafico_resposta_unica(
        sub: pd.DataFrame,
        textos_alternativo: dict,
        idx_pergunta: int) -> px.bar:
    """
    Obtém um gráfico de barras com as respostas de uma pergunta de unica escolha.

    Parâmetros:
    -----------
    sub:pd.DataFrame
        Dataframe com as respostas de uma pergunta de unica escolha.
    textos_alternativo:dict
        Dicionário com as respostas de uma pergunta de unica escolha.
    idx_pergunta:int
        Índice da pergunta de unica escolha.

    Retornos:
    ----------
    fig:px.bar
        Gráfico de barras com as respostas de uma pergunta de unica escolha.
    """

    sub['texto_curto'] = sub[sub.columns[0]].apply(
        lambda x: x if len(x) < 60 else x[0:60] + "...")
    fig = px.bar(sub, x='texto_curto', y=sub.columns[1],
                 labels={"texto_curto": textos_alternativo[idx_pergunta]},)
    return fig


def obter_grafico_resposta_multiplas(sub: pd.DataFrame) -> px.bar:
    """
    Obtém um gráfico de barras com as respostas de uma pergunta de multipla escolha.

    Parâmetros:
    -----------
    sub:pd.DataFrame
        Dataframe com as respostas de uma pergunta de multipla escolha.

    Retornos:
    ----------
    fig:px.bar
        Gráfico de barras com as respostas de uma pergunta de multipla escolha.
    """
    fig = px.bar(sub, x=sub.columns[0], y=sub.columns[1])
    return fig


def apresentar_analise_univariada(
        df: pd.DataFrame,
        tipo_pergunta: dict,
        resposta_multipla: dict,
        categoria_pergunta: dict,
        textos_alternativo: dict):
    """
    Apresenta a análise univariada.

    Parâmetros:
    -----------
    df:pd.DataFrame
        Dataframe com as respostas do questionário.
    tipo_pergunta:dict
        Dicionário com os tipos de perguntas.
    resposta_multipla:dict
        Dicionário com as respostas de perguntas de multipla escolha.
    categoria_pergunta:dict
        Dicionário com as categorias de perguntas.
    textos_alternativo:dict
        Dicionário com os textos alternativos para as perguntas.
    """

    # Cria um subheader para a analise univariada
    st.subheader("Análise Univariada")

    # Cria a caixa de seleção para a parte do dicionário 
    opcao_parte = st.sidebar.selectbox("Selecione a parte do questionário:", [
                                       ""] + list(dict_partes_questionario.keys()))
    # Cria a caixa de seleção o modo de exibição do gráfico/tabela
    qtde_perc = st.sidebar.selectbox("Apresentar quantidade ou percentual?", [
                                     "Quantidade", "Percentual"])

    # Se a parte do questionário for selecionada
    if opcao_parte != "":
        st.write(f"##### {opcao_parte}")

        # Cria o spinner enquanto os dados são processados
        with st.spinner('Processando...'):
            
            parte = dict_partes_questionario[opcao_parte]
            perguntas = categoria_pergunta[parte]
            
            # Para cada pergunta pertencente àquela parte do questionário
            for p in perguntas:

                # Exibe o texto da pergunta
                st.write(f"**{textos_alternativo[p]}**")

                # Se a pergunta for de multipla escolha
                if p in tipo_pergunta['multipla']:
                    sub = obter_dataframe_respostas_multiplas(df, resposta_multipla,
                                                              p, textos_alternativo, qtde_perc)

                    AgGrid(sub,
                           theme='material',
                           fit_columns_on_grid_load=True)

                    st.plotly_chart(obter_grafico_resposta_multiplas(
                        sub, textos_alternativo, p))
                    st.markdown(
                        "<small>**Observação:** Para perguntas de multiplas escolhas a soma das quantidades das respostas pode ultrapassar a quantidade de respondentes</small>", unsafe_allow_html=True)
                
                # Se a pergunta for de unica escolha
                else:
                    sub = obter_dataframe_resposta_unica(
                        df, p, textos_alternativo, qtde_perc)
                    AgGrid(sub,
                           theme='material',
                           fit_columns_on_grid_load=True)

                    st.plotly_chart(obter_grafico_resposta_unica(
                        sub, textos_alternativo, p))
