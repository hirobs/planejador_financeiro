import pandas as pd
from enums import TipoTransacao

def data_cleaning(df,origem:str, data_max):
        df = apagar_transacao(df,origem)
        nova_ordem_colunas = ['dt', 'categoria', 'descricao','parcela','valor','tipo_transacao']
        df = df[nova_ordem_colunas]
        # Selecionar linhas onde a coluna 'Data' é maior que a data da variável
        df = df[pd.to_datetime(df['dt'], format='%d/%m/%Y')> pd.to_datetime(data_max, format='%d/%m/%Y')]
        print("Quantidade de linhas:", len(df))

        return df

def apagar_transacao(df,origem):
    if origem == TipoTransacao.CARTAO:
        df.columns = ['dt', 'nome', 'final', 'categoria', 'descricao', 'parcela', 'valor_us','cotacao',  'valor']
        df.drop(columns=['nome','final','valor_us','cotacao'], inplace=True)
       
        palavras_a_apagar = ["pagamento fatura", "estorno tarifa", "anuidade diferenciada"]
        condicao_apagar = df['descricao'].str.contains('|'.join(palavras_a_apagar), case=False)
        df = df[~condicao_apagar]

        df.loc[:, 'tipo_transacao'] = origem.value

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
        palavras_a_apagar= ['saldo']
        condicao_apagar = df['descricao'].str.contains('|'.join(palavras_a_apagar), case=False)
        df = df[~condicao_apagar]

        df.loc[:, 'tipo_transacao'] = origem.value
        df['parcela'] = None
        df['categoria'] = None

        return df
    
#if __name__ == "__main__":

