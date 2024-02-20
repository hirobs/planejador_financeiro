import pandas as pd
import gspread
from tipo_transacao import TipoTransacao
#apagar depois
#gspread_credential = json.loads(st.secrets['gspreadsheet']['my_project_settings'])
#gspread_name = st.secrets['gspreadsheet']['SPREADSHEET_NAME']
#gc = gspread.service_account_from_dict(gspread_credential)

###
def conexao_gspread(credentials):
    gc = gspread.service_account_from_dict(credentials)
    return gc

def data_maxima(gc, origem, gspread_name):
    spreadsheet = gc.open(gspread_name)
 #   worksheet = spreadsheet.get_worksheet(0) 
    worksheet = spreadsheet.get_worksheet(1) 
    if origem == TipoTransacao.CONTA.value:
        max_date_cell = worksheet.cell(2, 1).value 
        return max_date_cell
    else:
        max_date_cell = worksheet.cell(2, 2).value  
        return max_date_cell

def inserir_planilha(df,spreadsheet_name, gc):
    #gc = conexao_gspread(credentials)
    planilha = gc.open(spreadsheet_name)
    
    nome_pagina = planilha.get_worksheet(0).title
    planilha.values_append(nome_pagina, {'valueInputOption': 'RAW'}, {'values': df.values.tolist()})
    return len(df)

#if __name__ == "__main__":
    #gc = conexao_gspread()
    #data_maxima(gc)
