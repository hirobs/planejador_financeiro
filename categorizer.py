import pandas as pd

def recategorizer(descricao):
    caminho_recategorizador = '/Users/hirobs/Library/CloudStorage/OneDrive-SharedLibraries-Onedrive/recategorizacao.xlsx'
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
    
def classificador(lista_transacao, titulo_arquivo = None, tipo_arquivo = None):

    # Classificar cada descrição na lista
    descricao = ''
    for transacao in lista_transacao:
        # Verificar se a descrição precisa de recategorização
        if tipo_arquivo == 'CARTAO':
            descricao = transacao[4]
        else:
            descricao = transacao[1]

        nova_categoria = recategorizer(descricao)
        if nova_categoria:
            transacao.append(nova_categoria)
        return transacao

def main():
    dados = [
        # Coloque aqui os dados que serão passados para a função classificador()
    ]

    classificador(dados)

if __name__ == "__main__":
    main()