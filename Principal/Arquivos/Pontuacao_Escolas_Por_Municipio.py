import pandas as pd
import numpy as np


def tabelasEscolasAno(ano):
    headInfraPadrao = ["ANO_CENSO","SIGLA","FK_COD_MUNICIPIO","ID_DEPENDENCIA_ADM","ID_SALA_PROFESSOR","ID_LABORATORIO_INFORMATICA",
                "ID_LABORATORIO_CIENCIAS","ID_QUADRA_ESPORTES_COBERTA","ID_QUADRA_ESPORTES_DESCOBERTA","ID_COZINHA","ID_BIBLIOTECA",
                "ID_AUDITORIO","ID_PATIO_COBERTO","ID_PATIO_DESCOBERTO","NUM_SALAS_EXISTENTES","NUM_EQUIP_TV","NUM_EQUIP_COPIADORA",
                "NUM_EQUIP_IMPRESSORA","NUM_EQUIP_SOM","NUM_EQUIP_MULTIMIDIA","NUM_COMP_ADMINISTRATIVOS",
                "NUM_COMP_ALUNOS","ID_INTERNET","NUM_FUNCIONARIOS","ID_ALIMENTACAO"]
    itensInfraPadrao = headInfraPadrao[4:]
    if ano == '2013':
        headInfra = headInfraPadrao
        itensInfra = itensInfraPadrao
        pesos = [20,50,40,50,25,20,40,25,30,15,5,3,10,5,10,4,5,3,20,10,40]
        sequencia = list(range(len(itensInfra)-1))
    
    if ano == '2015' or ano == '2017':    
        headInfra = ["NU_ANO_CENSO","CO_UF","CO_MUNICIPIO","TP_DEPENDENCIA","IN_SALA_PROFESSOR","IN_LABORATORIO_INFORMATICA",
                        "IN_LABORATORIO_CIENCIAS","IN_QUADRA_ESPORTES_COBERTA","IN_QUADRA_ESPORTES_DESCOBERTA","IN_COZINHA","IN_BIBLIOTECA",
                        "IN_AUDITORIO","IN_PATIO_COBERTO","IN_PATIO_DESCOBERTO","NU_SALAS_EXISTENTES","NU_EQUIP_TV","NU_EQUIP_COPIADORA",
                        "NU_EQUIP_IMPRESSORA","NU_EQUIP_SOM","NU_EQUIP_MULTIMIDIA","NU_COMP_ADMINISTRATIVO",
                        "NU_COMP_ALUNO","IN_INTERNET","NU_FUNCIONARIOS","IN_ALIMENTACAO"]
        itensInfra = headInfra[4:]
        pesos = [20,50,40,50,25,20,40,25,30,15,5,3,10,5,10,4,5,3,20,10,40]
        sequencia = list(range(len(itensInfra)-1))
    return headInfra, itensInfra, pesos, sequencia, headInfraPadrao, itensInfraPadrao

def agrupamento(x):
    result = {'ANO_CENSO': x['ANO_CENSO'].min(),
              'UF_PROPONENTE': x['SIGLA'].min(),
              'CD_GEOCUF': x['COD'].min(),
              'CD_GEOCODM': x['COD_MUNIC_IBGE'].min(),
              'MEDIA_PONTUACAO_ESCOLAS_POR_CIDADE': x['PONTUACAO_POR_ESCOLA'].mean()
    }
    return pd.Series(result)

def dadosEscolas(ano, itens):
    ESCOLAS = {
        'nome_arquivo_csv': './Dados/escolas'+ano+'.csv',
        'sep':'|',
        'encoding':'ISO-8859-1',
        'itens_tabelas_escolas': itens 
    }
    return ESCOLAS

def inserirNomeMunicipio(tabela):
    municipios = pd.read_csv('./Dados/municipios.csv',low_memory=False, encoding='ISO-8859-1', sep=';')
    municipios.rename(columns={'CD_GCMUN':'COD_MUNIC_IBGE'}, inplace=True)
    municipios = municipios[['COD_MUNIC_IBGE','NM_MUN_2017']]
    mergeTabelas = pd.merge(tabela, municipios, how='inner', on='COD_MUNIC_IBGE')
    return mergeTabelas

def inserirSiglaEstado(tabela):
    codEstado = pd.read_csv('./Dados/cod_estados.csv',low_memory=False, encoding='ISO-8859-1', sep=';')
    codEstado = codEstado[['SIGLA','COD']]
    mergeTabelas = pd.merge(tabela, codEstado, how='inner', on='COD')
    return mergeTabelas

def inserirCodEstadoBR(local, tabela):
    dfEstado = pd.read_csv('./Dados/cod_estados.csv',low_memory=False, encoding='ISO-8859-1', sep=';')
    dfEstado = dfEstado[['SIGLA','COD']]
    mergeTabelas = pd.merge(tabela, dfEstado, how='inner', on='SIGLA')
    return mergeTabelas

def inserirCodEstado(local, tabela):
    dfEstado = pd.read_csv('./Dados/cod_estados.csv',low_memory=False, encoding='ISO-8859-1', sep=';')
    dfEstado = dfEstado.loc[(dfEstado['SIGLA'] == local)]
    tabela["COD"] = int(dfEstado['COD'])
    return tabela

def gerarTabelaPontuacaoEscolas(local, ano):
    headInfra, itensInfra, pesos, sequencia, headInfraPadrao, itensInfraPadrao = tabelasEscolasAno(ano)
    ESCOLAS = dadosEscolas(ano, itensInfra)
    df_escola = pd.read_csv(ESCOLAS['nome_arquivo_csv'],low_memory=False, encoding=ESCOLAS['encoding'], sep=ESCOLAS['sep'])
    df_escola = df_escola[headInfra]
    df_escola = df_escola.fillna(0) #Converte NaN para 0

    if ano == '2013':
        if local != 'BR':
            df_escola = df_escola.loc[(df_escola['SIGLA'] == local)]
            df_escola = inserirCodEstado(local, df_escola)
        else:
            df_escola = inserirCodEstadoBR(local, df_escola)
    elif ano == '2015' or ano == '2017':
        df_escola.columns = headInfraPadrao
        headInfra = headInfraPadrao
        itensInfra = itensInfraPadrao
        df_escola.rename(columns={'SIGLA':'COD'}, inplace=True) #Nas escolas a partir de 2015 não vem a SIGLA vem o código do Estado
        df_escola = inserirSiglaEstado(df_escola)
        if local != 'BR':
            df_escola = df_escola.loc[(df_escola['SIGLA'] == local)]
        
    df_escola = df_escola.loc[(df_escola['ID_DEPENDENCIA_ADM'] == 3)] #Apenas escolas municipais
    df_escola = df_escola.copy()
    df_escola["PONTUACAO_POR_ESCOLA"] = sum( list(map(lambda x,y: x * df_escola[itensInfra[y]], pesos, sequencia)) )
    df_escola = df_escola[['ANO_CENSO', 'FK_COD_MUNICIPIO', 'PONTUACAO_POR_ESCOLA', 'SIGLA', 'COD']] 
    df_escola["FK_COD_MUNICIPIO"] = df_escola["FK_COD_MUNICIPIO"].astype("double")
    df_escola.rename(columns={'FK_COD_MUNICIPIO':'COD_MUNIC_IBGE'}, inplace=True)
    if local != 'BR':
        df_escolaAgrupada = df_escola.groupby('COD_MUNIC_IBGE')
    else:
        df_escolaAgrupada = df_escola.groupby('SIGLA')
    df_escolaPontuacao = df_escolaAgrupada.apply(agrupamento)
    df_escolaPontuacao.rename(columns={'size':'QTD_ESCOLAS'}, inplace=True)
    df_escolaPontuacao.rename(columns={'SIGLA':'UF_PROPONENTE'}, inplace=True)
    #df_escolaPontuacaoNome = inserirNomeMunicipio(df_escolaPontuacao)
    df_escolaPontuacao.to_csv('./Resultados/Tabelas/mediaPontuacaoEscolasPorMunicipio'+ano+'_'+local+'_out.csv',';')
    print('Tabela MediaPontuacaoEscolasPorMunicipios_'+ano+'_'+local+' gerada!')
    return df_escolaPontuacao

def gerarListaTabelasPontuacaoEscolas(estado, listaAnos):
    listaTabelasPontuacaoPorMunicipio = list(map(lambda x: gerarTabelaPontuacaoEscolas(estado, x), listaAnos))
    print('Todas as tabelas MediaPontuacaoEscolasPorMunicipios geradas!')
    print()
    return listaTabelasPontuacaoPorMunicipio
    
    
    

