# Imports gerais
import streamlit as st
import pandas as pd
import pickle

# Imports específicos (pacotes próprios)
from univariada import apresentar_analise_univariada
from multivariada import apresentar_analise_multivariada


# Função principal
def main():

    # Título do dashboard
    st.title("Dashboard - State of Data Brazil 2021")

    # Carga dos arquivos de dados
    # 1. Arquivo de dados principal
    df = pd.read_parquet('./data/df.parquet')

    # 2. Dicionário com o tipo de pergunta
    with open("./data/tipo_pergunta.pickle", "rb") as input_file:
        tipo_pergunta = pickle.load(input_file)

    # 3. Dicionário para perguntas de multipla escolha
    with open("./data/resposta_multipla.pickle", "rb") as input_file:
        resposta_multipla = pickle.load(input_file)

    # 4. Dicionário para a categoria da pergunta
    with open("./data/categoria_pergunta.pickle", "rb") as input_file:
        categoria_pergunta = pickle.load(input_file)

    # 5. Dicionario para os testes alternativos para perguntas e respostas
    with open("./data/textos_alternativo.pickle", "rb") as input_file:
       textos_alternativo = pickle.load(input_file)

    # 6. Dicionario para o índice das perguntas
    with open("./data/idx_perguntas.pickle", "rb") as input_file:
       idx_perguntas = pickle.load(input_file)

    # Seleção para o tipo de análise desejada (univariada ou multivariada)
    opcao_tipo_analise = st.sidebar.selectbox("Selecione o tipo de análise:", ["", 
        "Univariada", "Multivariada"])
    
    # Direciona para a análise univariada ou multivariada (conforme o caso)
    if opcao_tipo_analise == "Univariada":
        apresentar_analise_univariada(df, tipo_pergunta, resposta_multipla,
                    categoria_pergunta, textos_alternativo)
    elif opcao_tipo_analise == "Multivariada":
        apresentar_analise_multivariada(df, tipo_pergunta, resposta_multipla,
                    categoria_pergunta, textos_alternativo)

######################################################################################
if __name__ == '__main__':

    # Configurações gerais do Streamlit
    st.set_page_config(page_title="Dashboard - State of Data Brazil 2021", 
    layout="wide", initial_sidebar_state="expanded")

    # Remove o menu lateral do Streamlit
    hide_menu_style = """
            <style>
            #MainMenu {visibility: hidden;}
            </style>
            """
    st.markdown(hide_menu_style, unsafe_allow_html=True)

    # Imagem de capa do dashboard
    url_image = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTVaHohyAwyO6nb7L8UnzXqHFSfDSySfscwz2f_qomKovxz9Q7Pd2lhKVS09_DIwHVlq5Y&usqp=CAU"
    st.sidebar.markdown(f"![Image Description]({url_image})", unsafe_allow_html=True)

    main()


    ######################################################################################
    # Disclaimers do dashboard
    ######################################################################################

    # Laterais
    url = "https://www.datahackers.com.br/"
    st.sidebar.markdown("""<small>**Atenção:** Este é um trabalho independente, 
                de propósito meramente didático, e não possui qualquer 
                associação com a marca/comunidade [Data Hackers](%s) ou State of Data Brazil.</small>"""%url, 
                unsafe_allow_html=True)


    #######################################################################################
    # Rodapé
    url = "https://www.datahackers.com.br/"
    st.markdown("""<small>**Atenção:** Este é um trabalho independente, 
                de propósito meramente didático, e não possui quaisquer 
                associação com a marca/comunidade [Data Hackers](%s) ou State of Data Brazil.</small>"""%url, 
                unsafe_allow_html=True)

    url = "https://www.kaggle.com/datasets/datahackers/state-of-data-2021"
    st.markdown("<small>**Fonte dos dados**: [link](%s)</small>"% url, unsafe_allow_html=True)

    url = "https://www.stateofdata.com.br/"
    st.markdown("<small>**State of data Brazil 2021**: [link](%s)</small>"% url, unsafe_allow_html=True)

    url = "https://github.com/professortavares/desafio_datahackers"
    st.markdown("""<small>**Código fonte do dashboard**: [Github](%s)</small>"""%url, 
                unsafe_allow_html=True)

    url = "https://www.kaggle.com/leodaniel"
    st.markdown("""<small>**Meu perfil no** [Kaggle](%s)</small>"""%url, 
                unsafe_allow_html=True)
