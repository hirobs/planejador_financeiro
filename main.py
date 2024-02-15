import pandas as pd
import streamlit as st
from categorizer import classificador
import data_cleaning as dc
from tipo_transacao import TipoTransacao
from planilha import inserir_planilha
import json


def main():
    st.title("Validador de CSV/Excel v1")
    opcoes_combobox = ['Escolha', TipoTransacao.CONTA.value, TipoTransacao.CARTAO.value]
    escolha_combobox = st.selectbox("Escolha uma opção", opcoes_combobox)
    gspread_credential = json.loads(st.secrets['gspreadsheet']['my_project_settings'])
    gspread_name = st.secrets['gspreadsheet']['SPREADSHEET_NAME']

    uploaded_file = None

    if escolha_combobox != 'Escolha':
        uploaded_file = st.file_uploader("Escolha um arquivo CSV ou Excel", type=["csv", "xlsx","xls"])

    if uploaded_file is not None:
        try:
            df = pd.DataFrame()
            if uploaded_file.type == 'application/vnd.ms-excel':
                df = dc.data_cleaning(pd.read_excel(uploaded_file, dtype='str'), TipoTransacao.CONTA)
                df = classificador(df)
                st.write(df.head())
                
                inserir_planilha(df,gspread_credential,gspread_name)
            else:
                df = dc.data_cleaning(pd.read_csv(uploaded_file, dtype='str',sep=';'),TipoTransacao.CARTAO)
                df = classificador(df)
                st.write(df.head())
                
                inserir_planilha(df,gspread_credential,gspread_name)

            st.success("Arquivo carregado com sucesso!")


        except Exception as e:
            st.error(f"Erro ao carregar o arquivo: {e}")

if __name__ == "__main__":
    main()
