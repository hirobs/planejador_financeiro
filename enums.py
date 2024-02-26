from enum import Enum

class TipoTransacao(Enum):
    CARTAO = 'CARTAO'
    CONTA = 'CONTA_CORRENTE'

class TipoAba(Enum):
    DADOS = 0
    DATA_MAX = 1
    CATEGORIA = 2
