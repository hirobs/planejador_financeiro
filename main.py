import pandas as pd
import streamlit as st
from categorizer import classificador,adicionar_categoria
import data_cleaning as dc
from enums import TipoTransacao, TipoAba
import planilha
import json


gc = ''
gspread_name = ''
# Inicializando session_state
if "estado_atual" not in st.session_state:
    st.session_state.estado_atual = "tela_adicionar_dados"
    st.session_state.escolha_combobox_adicionar_dados = 'Escolha'

def tela_adicionar_dados():
    opcoes_combobox = ['Escolha', TipoTransacao.CONTA.value, TipoTransacao.CARTAO.value]
    escolha_combobox = st.selectbox("Escolha uma opção", opcoes_combobox, key='combobox_adicionar_dados', 
                                    index=opcoes_combobox.index(st.session_state.escolha_combobox_adicionar_dados))
    st.session_state.escolha_combobox_adicionar_dados = escolha_combobox
    st.session_state.update({"estado_atual": "tela_adicionar_dados"})
    if escolha_combobox != 'Escolha':
        uploaded_file = st.file_uploader("Escolha um arquivo CSV ou Excel", type=["csv", "xlsx", "xls"])

        if uploaded_file is not None:
            try:
                gc = planilha.conexao_gspread(json.loads(st.secrets['gspreadsheet']['my_project_settings']))
                gspread_name = st.secrets['gspreadsheet']['SPREADSHEET_NAME']
                linha = 0
                df = pd.DataFrame()

                if uploaded_file.type == 'application/vnd.ms-excel':
                    data_max = planilha.data_maxima(gc, TipoTransacao.CONTA.value, gspread_name)
                    df = dc.data_cleaning(pd.read_excel(uploaded_file, dtype='str'), TipoTransacao.CONTA, data_max)
                else:
                    data_max = planilha.data_maxima(gc, TipoTransacao.CARTAO.value, gspread_name)
                    df = dc.data_cleaning(pd.read_csv(uploaded_file, dtype='str', sep=';'), TipoTransacao.CARTAO, data_max)

                df = classificador(df, gc, gspread_name)
                st.write(df.head())

                linha = planilha.inserir_planilha(df, gspread_name, gc)

                st.success(f"Arquivo carregado com sucesso! Quantidade de linha(s) inserida(s): {linha}")

            except Exception as e:
                st.error(f"Erro ao carregar o arquivo: {e}")

def tela_adicionar_categoria():
    global gc, gspread_name 
    st.session_state.update({"estado_atual": "tela_adicionar_categoria"})

    submit = False
    descricao = ''
    categoria = ''

    with st.form("Form"): 
        descricao = st.text_input("Descrição:")
        categoria = st.text_input("Categoria:")
        submit = st.form_submit_button("Submit")
    if submit:  
        if descricao != "" and categoria != "":
                if gc == "" and gspread_name == "":
                    gc = planilha.conexao_gspread(json.loads(st.secrets['gspreadsheet']['my_project_settings']))
                    gspread_name = st.secrets['gspreadsheet']['SPREADSHEET_NAME']

                adicionar_categoria(gc,gspread_name,descricao,categoria)
                st.success(f"Categoria '{descricao}' adicionada com sucesso na categoria '{categoria}'")
        else: 
            st.error("Favor preencher a categoria e descrição")

def tela_editar_categoria():
    st.session_state.update({"estado_atual": "tela_editar_categoria"})
    st.write('oioi editar categoria')

tela_atual = st.session_state.estado_atual

# Botão
botao_adicionar_dado = st.sidebar.button("Adicionar Dado", key="adicionar_dado", use_container_width=True)
botao_adicionar_categoria = st.sidebar.button("Adicionar Categoria", key="adicionar_categoria", use_container_width=True)
botao_editar_categoria = st.sidebar.button("Editar Categoria", key="editar_categoria", use_container_width=True)

if botao_adicionar_dado:
    tela_atual = "tela_adicionar_dados"
    st.session_state.estado_atual = tela_atual
elif botao_adicionar_categoria:
    tela_atual = "tela_adicionar_categoria"
    st.session_state.estado_atual = tela_atual
elif botao_editar_categoria:
    tela_atual = "tela_editar_categoria"
    st.session_state.estado_atual = tela_atual

st.markdown(f"# Tela Atual: {tela_atual}")

if tela_atual == "tela_adicionar_dados":
    tela_adicionar_dados()
elif tela_atual == "tela_adicionar_categoria":
    tela_adicionar_categoria()
elif tela_atual == "tela_editar_categoria":
    tela_editar_categoria()
