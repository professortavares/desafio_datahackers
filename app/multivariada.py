# Imports gerais
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from st_aggrid import AgGrid

# Imports específicos
from reuse import dict_partes_questionario


def apresentar_resultado_unica_multiplos(
    df:pd.DataFrame, 
    idx_pergunta1:int, 
    idx_pergunta2:int,
    textos_alternativo:dict, 
    resposta_multipla:dict):
    """
    Apresenta o resultado de uma questão de uma única resposta para múltiplas respostas.

    Parâmetros
    ----------
    df: pd.DataFrame
        Dataframe com as respostas.
    idx_pergunta1: int
        Índice da questão de uma única resposta.
    idx_pergunta2: int
        Índice da questão de múltiplas respostas.
    textos_alternativo: dict
        Dicionário com os textos das alternativas.
    resposta_multipla: dict
        Dicionário com os índices das questões de múltiplas respostas.
    """

    # Subset da tabela com as respostas
    df_2 = df.copy()

    # Altera o nome das colunas para os textos das alternativas
    df_2 = df_2.rename(
        columns={df_2.columns[idx_pergunta1]: textos_alternativo[idx_pergunta1]})
    for c in resposta_multipla[idx_pergunta2]:
        df_2 = df_2.rename(columns={df_2.columns[c]: textos_alternativo[c]})

    # Prepara o dataframe para agrupar as respostas
    cols = [df_2.columns[idx_pergunta1]] + \
        list(df_2.columns[resposta_multipla[idx_pergunta2]])
    r = df_2[cols]
    r_agg = r.groupby(r.columns[0]).sum()
    st.table(r_agg)

    # Exibe o gráfico
    fig = px.imshow(r_agg, text_auto=True, labels=dict(color="Quantidade"))
    st.plotly_chart(fig)


def apresentar_resultado_multios_unica(
    df:pd.DataFrame, 
    idx_pergunta1:int, 
    idx_pergunta2:int,
    textos_alternativo:dict, 
    resposta_multipla:dict):
    """
    Apresenta o resultado de uma questão de múltiplas respostas para uma única resposta.

    Parâmetros
    ----------
    df: pd.DataFrame
        Dataframe com as respostas.
    idx_pergunta1: int
        Índice da questão de múltiplas respostas.
    idx_pergunta2: int
        Índice da questão de uma única resposta.
    textos_alternativo: dict
        Dicionário com os textos das alternativas.
    resposta_multipla: dict
        Dicionário com os índices das questões de uma única resposta.
    """

    # Subset da tabela com as respostas
    df_2 = df.copy()

    # Altera o nome das colunas para os textos das alternativas
    df_2 = df_2.rename(
        columns={df_2.columns[idx_pergunta2]: textos_alternativo[idx_pergunta2]})
    for c in resposta_multipla[idx_pergunta1]:
        df_2 = df_2.rename(columns={df_2.columns[c]: textos_alternativo[c]})

    # Prepara o dataframe para agrupar as respostas
    cols = [df_2.columns[idx_pergunta2]] + \
        list(df_2.columns[resposta_multipla[idx_pergunta1]])
    r = df_2[cols]
    r_agg = r.groupby(r.columns[0]).sum()
    st.table(r_agg.T)

    # Exibe o gráfico
    fig = px.imshow(r_agg.T, text_auto=True, labels=dict(color="Quantidade"))
    st.plotly_chart(fig)


def apresentar_resultado_unica_unica(
    df:pd.DataFrame, 
    idx_pergunta1:int, 
    idx_pergunta2:int,
    textos_alternativo:dict):
    """
    Apresenta o resultado de uma questão de uma única resposta para uma única resposta.

    Parâmetros
    ----------
    df: pd.DataFrame
        Dataframe com as respostas.
    idx_pergunta1: int
        Índice da questão de uma única resposta.
    idx_pergunta2: int
        Índice da questão de uma única resposta.
    textos_alternativo: dict
        Dicionário com os textos das alternativas.
    """

    # Subset da tabela com as respostas
    sub = df[[df.columns[idx_pergunta1], df.columns[idx_pergunta2]]]
    sub['c'] = 1
    sub_agg = sub.groupby(
        [df.columns[idx_pergunta1], df.columns[idx_pergunta2]]).agg('count')[['c']]
    sub_agg = sub_agg.reset_index()
    sub_agg.rename(columns={'c': 'Quantidade',
                            sub_agg.columns[0]: textos_alternativo[idx_pergunta1],
                            sub_agg.columns[1]: textos_alternativo[idx_pergunta2]}, inplace=True)
    sub_agg = sub_agg.sort_values(
        by=['Quantidade'], ascending=False, ignore_index=True)
    AgGrid(sub_agg,
           theme='material',
           fit_columns_on_grid_load=True)

    # Exibe o gráfico
    fig = px.bar(
        sub_agg, x=sub_agg.columns[0], y="Quantidade", color=sub_agg.columns[1])
    st.plotly_chart(fig)

    fig = px.histogram(sub_agg, x=sub_agg.columns[0], y="Quantidade",
                       color=sub_agg.columns[1], barnorm="percent")
    fig.update_layout(
        yaxis_title="Percentual(%)",
    )
    st.plotly_chart(fig)


def apresentar_analise_multivariada(
    df:pd.DataFrame, 
    tipo_pergunta:dict, 
    resposta_multipla:dict,
    categoria_pergunta:dict, 
    textos_alternativo:dict):
    """
    Apresenta o resultada da análise multivariada.

    Parâmetros
    ----------
    df: pd.DataFrame
        Dataframe com as respostas.
    tipo_pergunta: dict
        Dicionário com os tipos de pergunta.
    resposta_multipla: dict
        Dicionário com os índices das questões de múltiplas respostas.
    categoria_pergunta: dict
        Dicionário com os índices das questões de categoria.
    textos_alternativo: dict
        Dicionário com os textos das alternativas.
    """

    pergunta_var1 = ""
    pergunta_var2 = ""

    # Seleção da primeira questão (variável)
    st.sidebar.write("**Variável 1:**")
    opcao_parte1 = st.sidebar.selectbox("Selecione a parte do questionário:", [
                                        ""] + list(dict_partes_questionario.keys()), key="parte_var1")

    # Caso seja selecionada uma parte do questionário
    if opcao_parte1 != "":
        parte1 = dict_partes_questionario[opcao_parte1]
        perguntas1 = categoria_pergunta[parte1]
        textos_perguntas1 = [textos_alternativo[p] for p in perguntas1]
        pergunta_var1 = st.sidebar.selectbox("Selecione a pergunta da primeira variável:", [
                                             ""] + textos_perguntas1, key="perg_var1")

    # Seleção da primeira questão (variável)
    st.sidebar.write("**Variável 2:**")
    opcao_parte2 = st.sidebar.selectbox("Selecione a parte do questionário:", [
                                        ""] + list(dict_partes_questionario.keys()), key="parte_var2")
    # Caso seja selecionada uma parte do questionário
    if opcao_parte2 != "":
        parte2 = dict_partes_questionario[opcao_parte2]
        perguntas2 = categoria_pergunta[parte2]
        textos_perguntas2 = [textos_alternativo[p] for p in perguntas2]
        pergunta_var2 = st.sidebar.selectbox("Selecione a pergunta da primeira variável:", [
                                             ""] + textos_perguntas2, key="perg_var2")

    # Caso as perguntas tenham sido selecionadas
    if pergunta_var1 != "" and pergunta_var2 != "":
        # Se as perguntas forem iguais
        if pergunta_var1 == pergunta_var2:
            # Exibe mensagem de erro
            st.error("Por favor, selecione perguntas distintas.")
        # Se as perguntas forem diferentes
        else:
            # Processamento da análise multivariada
            idx_pergunta1 = textos_alternativo.index(pergunta_var1)
            idx_pergunta2 = textos_alternativo.index(pergunta_var2)

            st.write(f"**Variável 1: {pergunta_var1}**")
            st.write(f"**Variável 2: {pergunta_var2}**")

            # Seleciona o tipo correto da analise multivariada
            if idx_pergunta1 in tipo_pergunta['unica'] and \
               idx_pergunta2 in tipo_pergunta['unica']:

                apresentar_resultado_unica_unica(df, idx_pergunta1,
                                                 idx_pergunta2, textos_alternativo)
            elif idx_pergunta1 in tipo_pergunta['unica'] and \
                    idx_pergunta2 in tipo_pergunta['multipla']:

                apresentar_resultado_unica_multiplos(df, idx_pergunta1, idx_pergunta2,
                                                     textos_alternativo, resposta_multipla)

            elif idx_pergunta1 in tipo_pergunta['multipla'] and \
                    idx_pergunta2 in tipo_pergunta['unica']:
                apresentar_resultado_multios_unica(df, idx_pergunta1, idx_pergunta2,
                                                   textos_alternativo, resposta_multipla)

            else:
                # Débito técnico
                # TODO: implementar o caso de perguntas de múltiplas respostas e categoria
                st.info("A exibição entre respostas para perguntas de múltiplas escolhas ainda não foi implementada.")
