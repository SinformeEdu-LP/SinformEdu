import pandas as pd
import numpy as np

def agrupamento(x):
    result = {'ANO': x['ANO'].min(),
              'TOTAL_VL_GLOBAL_PROP': x['VL_GLOBAL_PROP'].sum()
    }
    return pd.Series(result)

def convenioPropostaPorLocal(local, ano):
    df = pd.read_csv('./Dados/dfConvenioProposta.csv',low_memory=False, sep=';')
    df = df.loc[(df['ANO'] == int(ano) )] 
    if local != 'BR':
        df = df.loc[(df['UF_PROPONENTE'] == local)]
        dfAgrupada = df.groupby('COD_MUNIC_IBGE')
        df_result = dfAgrupada.apply(agrupamento)
    else:
        dfAgrupada = df.groupby('UF_PROPONENTE')
        df_result = dfAgrupada.apply(agrupamento)
    
    return df_result

def mergeEscolasConvenios(local, ano, tabelaEscolas):
    if local != 'BR':
        valor = 'COD_MUNIC_IBGE'
    else:
        valor = 'UF_PROPONENTE'
    convProposta = convenioPropostaPorLocal(local, ano)
    escolasConvenios = pd.merge(tabelaEscolas, convProposta, how='left', on=valor)
    escolasConvenios = escolasConvenios.fillna(0) #Converte NaN para 0
    return escolasConvenios

def gerarListaEscolasConvenios(local, listaTabelaEscolas, ano):
    listaEscolasConvenios = list(map(lambda x: mergeEscolasConvenios(local, ano, x), listaTabelaEscolas))
    return listaEscolasConvenios
    
    
    

