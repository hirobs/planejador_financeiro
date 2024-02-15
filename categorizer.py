import pandas as pd

def recategorizador(descricao):
    caminho_recategorizador = 'aux/recategorizacao.xlsx'
    # Carregar o arquivo Excel em um DataFrame do pandas
    
    df_recategorizador = pd.read_excel(caminho_recategorizador)
    

    # Converter a coluna 'descricao' para letras minúsculas para realizar a comparação
    df_recategorizador['descricao'] = df_recategorizador['descricao'].str.lower()

    # Procurar pela descrição no DataFrame
    resultado = df_recategorizador.loc[df_recategorizador['descricao'].apply(lambda x: x.lower() in descricao.lower()), 'categoria']

    # Se a descrição foi encontrada, retornar a categoria correspondente
    if not resultado.empty:
        return resultado.iloc[0]
    

    return None
    
def classificador(df):
    df_copia = df.copy()
    for indice, transacao in df_copia.iterrows():
        descricao = transacao['descricao']

        nova_categoria = recategorizador(descricao)

        if nova_categoria:
            df_copia.at[indice, 'categoria'] = nova_categoria

    return df_copia

if __name__ == "__main__":
    recategorizador()