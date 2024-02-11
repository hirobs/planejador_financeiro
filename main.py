import pandas as pd
import streamlit as st
from categorizer import classificador
import data_cleaning as dc


def main():
    st.title("Validador de CSV/Excel")

    uploaded_file = st.file_uploader("Escolha um arquivo CSV ou Excel", type=["csv", "xlsx","xls"])

    if uploaded_file is not None:
        try:
            # Tenta carregar o arquivo como DataFrame
            df = pd.DataFrame()
            #df = pd.read_csv(uploaded_file) if uploaded_file.type == 'application/vnd.ms-excel' else pd.read_excel(uploaded_file)
            st.write(uploaded_file.type)
            if uploaded_file.type == 'application/vnd.ms-excel':
                #todo
                df = pd.read_excel(uploaded_file, dtype='str')
            else:
                df = pd.read_csv(uploaded_file, dtype='str')


            # Se o carregamento for bem-sucedido, exibe uma mensagem de sucesso
            st.success("Arquivo carregado com sucesso!")

            # Exibe informações básicas sobre o DataFrame
            st.write("Principais estatísticas do DataFrame:")
            st.write(df.describe())

        except Exception as e:
            # Se ocorrer uma exceção, exibe uma mensagem de erro
            st.error(f"Erro ao carregar o arquivo: {e}")

if __name__ == "__main__":
    main()
