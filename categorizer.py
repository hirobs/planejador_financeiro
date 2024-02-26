import pandas as pd
import warnings
import planilha
from enums import TipoAba

# def recategorizador(descricao):
#     caminho_recategorizador = 'aux/recategorizacao.xlsx'
#     # Carregar o arquivo Excel em um DataFrame do pandas
#     warnings.simplefilter(action='ignore', category=UserWarning)
#     df_recategorizador = pd.read_excel(caminho_recategorizador)
    

#     # Converter a coluna 'descricao' para letras minúsculas para realizar a comparação
#     df_recategorizador['descricao'] = df_recategorizador['descricao'].str.lower()

#     # Procurar pela descrição no DataFrame
#     resultado = df_recategorizador.loc[df_recategorizador['descricao'].apply(lambda x: x.lower() in descricao.lower()), 'categoria']

#     # Se a descrição foi encontrada, retornar a categoria correspondente
#     if not resultado.empty:
#         return resultado.iloc[0]
    

#     return None
    
def classificador(df, gc,spreadsheet_name,retornar_dict = False):
    #df_copia = planilha.obter_planilha(gc,spreadsheet_name)
    df_copia = df.copy()
    df_categoria = planilha.obter_planilha(gc,spreadsheet_name, TipoAba.CATEGORIA)

    for indice, transacao in df_copia.iterrows():
        descricao = transacao['descricao']

        #caminho_recategorizador = 'aux/recategorizacao.xlsx'
        # Carregar o arquivo Excel em um DataFrame do pandas
        #warnings.simplefilter(action='ignore', category=UserWarning)
        #df_recategorizador = pd.read_excel(caminho_recategorizador)
        

        # Converter a coluna 'descricao' para letras minúsculas para realizar a comparação
        df_categoria['descricao'] = df_categoria['descricao'].str.lower()

        # Procurar pela descrição no DataFrame
        resultado = df_categoria.loc[df_categoria['descricao'].apply(lambda x: x.lower() in descricao.lower()), 'categoria']

        # Se a descrição foi encontrada, retornar a categoria correspondente
        linhas_modificadas = []

        nova_categoria = None
        if not resultado.empty:
            nova_categoria =  resultado.iloc[0]
            linhas_modificadas.append({'row':indice,'categoria':nova_categoria})
            df_copia.at[indice, 'categoria'] = nova_categoria
    if retornar_dict:
        linhas_modificadas
    else:
        return df_copia

def classificador_total(gc,spreadsheet_name):
    df = planilha.obter_planilha(gc,spreadsheet_name, TipoAba.DADOS)
    df = classificador(df,gc,spreadsheet_name)
    return df

# if __name__ == "__main__":
#     recategorizador()