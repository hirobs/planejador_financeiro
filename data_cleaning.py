import pandas as pd
from tipo_transacao import TipoTransacao

def data_cleaning(df,origem:str):
        df = apagar_transacao(df,origem)

def apagar_transacao(df,origem):
    if origem == TipoTransacao.CARTAO:
        df.drop(columns=['Nome no Cartão','Final do Cartão','Valor (em US$)','Cotação (em R$)'], inplace=True)
        df.rename(columns={'Data de Compra': 'dt', 'Descrição': 'descricao', 
                           'Valor (em R$)': 'valor', 'Parcela': 'parcela', 'Categoria': 'categoria'}, inplace=True)
        
        palavras_a_apagar = ["pagamento fatura", "estorno tarifa", "anuidade diferenciada"]
        condicao_apagar = df['descricao'].str.contains('|'.join(palavras_a_apagar), case=False)
        df = df[~condicao_apagar]

        df['tipo_transacao'] = TipoTransacao.CARTAO.value

        return df
    
    elif origem == TipoTransacao.CONTA:
        df.columns = ['dt', 'descricao', 'conta', 'valor', 'saldo']
        df.drop(columns=['saldo', 'conta'],inplace = True)
        #Apaga as linhas iniciais para limpar
        df = df.drop(range(9))
        index_max = df[df['dt'] == 'lançamentos futuros'].index.max()
        df = df.loc[:index_max-1]
        df = df.reset_index(drop=True)
        #Apagar as informações de saldo
        palavras_a_apagar= ['saldo','asd']
        condicao_apagar = df['descricao'].str.contains('|'.join(palavras_a_apagar), case=False)
        df = df[~condicao_apagar]

        df['parcela'] = None
        df['categoria'] = None


        return df
    
if __name__ == "__main__":
    #df_fatura = pd.read_csv('/Users/hirobs/Downloads/Fatura_2024-02-10.csv', dtype='str', sep = ';')
    caminho = '/Users/hirobs/Downloads/Extrato Conta Corrente-120220242104.xls'
    df = pd.read_excel(caminho)
    data_cleaning(df,TipoTransacao.CONTA)

    #data_cleaning(df_fatura, TipoTransacao.CARTAO)
