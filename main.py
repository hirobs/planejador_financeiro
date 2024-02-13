import pandas as pd
import streamlit as st
from categorizer import classificador
import data_cleaning as dc
from tipo_transacao import TipoTransacao


def main():
    st.title("Validador de CSV/Excel v1")
    opcoes_combobox = ['Escolha', TipoTransacao.CONTA.value, TipoTransacao.CARTAO.value]
    escolha_combobox = st.selectbox("Escolha uma opção", opcoes_combobox)

    uploaded_file = None

    if escolha_combobox != 'Escolha':
        uploaded_file = st.file_uploader("Escolha um arquivo CSV ou Excel", type=["csv", "xlsx","xls"])

    if uploaded_file is not None:
        try:
            # Tenta carregar o arquivo como DataFrame
            df = pd.DataFrame()

            if uploaded_file.type == 'application/vnd.ms-excel':
                df = dc.data_cleaning(pd.read_excel(uploaded_file, dtype='str'), TipoTransacao.CONTA)
                print('saiu)')
                st.write(df.head())
            else:
                df = dc.data_cleaning(pd.read_csv(uploaded_file, dtype='str',sep=';'),TipoTransacao.CARTAO)
                st.write(df.head())


            # Se o carregamento for bem-sucedido, exibe uma mensagem de sucesso
            st.success("Arquivo carregado com sucesso!")

            # Exibe informações básicas sobre o DataFrame
            #st.write("Principais estatísticas do DataFrame:")
            #st.write(df.describe())

        except Exception as e:
            # Se ocorrer uma exceção, exibe uma mensagem de erro
            st.error(f"Erro ao carregar o arquivo: {e}")

if __name__ == "__main__":
    main()
