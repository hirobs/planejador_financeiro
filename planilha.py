import pandas as pd
import gspread
from enums import TipoTransacao, TipoAba
#apagar depois
import json
from streamlit import secrets
import re


gspread_credential = json.loads(secrets['gspreadsheet']['my_project_settings'])
gspread_name = secrets['gspreadsheet']['SPREADSHEET_NAME']
gc = gspread.service_account_from_dict(gspread_credential)

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

def obter_planilha(gc,spreadsheet_name, tipo_aba = TipoAba):
    spreadsheet = gc.open(spreadsheet_name)
    worksheet = spreadsheet.get_worksheet(tipo_aba.value)
    dados = worksheet.get_all_values()
    df = pd.DataFrame(dados[1:], columns=dados[0])
    return df 

def teste_procura_palavra():
    # palavra = 'ana'
    # criterio = re.compile(fr'\w*{re.escape(palavra)}\w*', re.IGNORECASE)
    # cell_list = worksheet.findall(criterio, in_column=3)
    # for cell in cell_list:
    #     print('linha '+ str(cell.row)+' coluna '+ str(cell.col) + ' palavra ' +str(cell.value)) 




    #linhas_para_atualizar = [3,4]  # Substitua pelos números das linhas que deseja atualizar
    #nova_informacao = "Nova Informação"  # Substitua pela nova informação que deseja adicionar
    pass

def atualizar_planilha(linhas_modificadas,gc,spreadsheet_name, tipo_aba = TipoAba ):
    spreadsheet = gc.open(gspread_name)
    worksheet = spreadsheet.get_worksheet(tipo_aba.value) 

    # Construir a lista de atualizações em lote
    atualizacoes_em_lote = []
    for linha in linhas_modificadas:
        celula = f"B{linha['row']}"  # Substitua 'B' pela letra da coluna desejada
        nova_informacao = linha['categoria']
        atualizacoes_em_lote.append({
            'range': celula,
            'values': [[nova_informacao]]
        })

    worksheet.batch_update(atualizacoes_em_lote)


if __name__ == "__main__":
    #gc = conexao_gspread()
    #data_maxima(gc)
    teste = [{'row':2,'categoria':'batata'},{'row':10,'categoria':'batata'}]
    atualizar_planilha(teste,gc,gspread_name,TipoAba.DADOS)
    print('a')
