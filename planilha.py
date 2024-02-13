import os
from dotenv import load_dotenv
import pandas as pd
import gspread
#from gspread_dataframe import set_with_dataframe

def inserir_planilha(df,credentials,spreadsheet_name):
    load_dotenv()

    # Acesse as variáveis de ambiente
    #credentials_path = os.getenv("GOOGLE_SHEETS_API_CREDENTIALS")
    #spreadsheet_name = os.getenv("SPREADSHEET_NAME")

    #dados = {'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]}
    #df = pd.DataFrame(dados)
    gc = gspread.service_account_from_dict(credentials)


    planilha = gc.open(spreadsheet_name)
    
    nome_pagina = planilha.get_worksheet(0).title
    planilha.values_append(nome_pagina, {'valueInputOption': 'RAW'}, {'values': df.values.tolist()})



if __name__ == "__main__":
    inserir_planilha()