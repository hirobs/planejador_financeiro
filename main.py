import pandas as pd
import streamlit as st
from categorizer import classificador
import data_cleaning as dc
from tipo_transacao import TipoTransacao
import planilha
import json


def main():
    st.title("Validador de CSV/Excel v1")
    opcoes_combobox = ['Escolha', TipoTransacao.CONTA.value, TipoTransacao.CARTAO.value]
    escolha_combobox = st.selectbox("Escolha uma opção", opcoes_combobox)
    gspread_credential = json.loads(st.secrets['gspreadsheet']['my_project_settings'])
    gspread_name = st.secrets['gspreadsheet']['SPREADSHEET_NAME']
    gc = ''

    uploaded_file = None

    if escolha_combobox != 'Escolha':
        uploaded_file = st.file_uploader("Escolha um arquivo CSV ou Excel", type=["csv", "xlsx","xls"])

    if uploaded_file is not None:
        gc = planilha.conexao_gspread(gspread_credential)
        linha = 0
        try:
            df = pd.DataFrame()
            if uploaded_file.type == 'application/vnd.ms-excel':
                data_max = planilha.data_maxima(gc,TipoTransacao.CONTA.value,gspread_name)
                df = dc.data_cleaning(pd.read_excel(uploaded_file, dtype='str'), TipoTransacao.CONTA, data_max)
                df = classificador(df)
                st.write(df.head())         
                
                linha = planilha.inserir_planilha(df,gspread_name, gc)
            else:
                data_max = planilha.data_maxima(gc,TipoTransacao.CARTAO.value,gspread_name)
                df = dc.data_cleaning(pd.read_csv(uploaded_file, dtype='str',sep=';'),TipoTransacao.CARTAO, data_max)
                df = classificador(df)
                st.write(df.head())
                
                linha = planilha.inserir_planilha(df,gspread_name, gc)

            st.success(f"Arquivo carregado com sucesso! Quantidade de linha(s) inserida(s): {linha}")


        except Exception as e:
            st.error(f"Erro ao carregar o arquivo: {e}")

if __name__ == "__main__":
    main()
