import pandas as pd
import gspread

def inserir_planilha(df,credentials,spreadsheet_name):
    #dados = {'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]}
    #df = pd.DataFrame(dados)
    gc = gspread.service_account_from_dict(credentials)

    planilha = gc.open(spreadsheet_name)
    
    nome_pagina = planilha.get_worksheet(0).title
    planilha.values_append(nome_pagina, {'valueInputOption': 'RAW'}, {'values': df.values.tolist()})

if __name__ == "__main__":
    inserir_planilha()