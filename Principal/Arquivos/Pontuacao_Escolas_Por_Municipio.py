import pandas as pd
import numpy as np

TabelaInfra = ["ANO_CENSO","SIGLA","FK_COD_MUNICIPIO","ID_DEPENDENCIA_ADM","ID_SALA_PROFESSOR","ID_LABORATORIO_INFORMATICA",
                "ID_LABORATORIO_CIENCIAS","ID_QUADRA_ESPORTES_COBERTA","ID_QUADRA_ESPORTES_DESCOBERTA","ID_COZINHA","ID_BIBLIOTECA",
                "ID_AUDITORIO","ID_PATIO_COBERTO","ID_PATIO_DESCOBERTO","NUM_SALAS_EXISTENTES","NUM_EQUIP_TV","NUM_EQUIP_COPIADORA",
                "NUM_EQUIP_IMPRESSORA","NUM_EQUIP_SOM","NUM_EQUIP_MULTIMIDIA","NUM_COMPUTADORES","NUM_COMP_ADMINISTRATIVOS",
                "NUM_COMP_ALUNOS","ID_INTERNET","NUM_FUNCIONARIOS","ID_ALIMENTACAO"]
ItensInfra = TabelaInfra[4:]
pesos = [20,50,40,50,25,20,40,25,30,15,5,3,10,5,10,4,3,5,3,20,10,40]
sequencia = list(range(len(ItensInfra)-1))

ESCOLAS_2013 = {
    'nome_arquivo_csv': '~/Documentos/Pandas Testes/escolas2013.csv',
    'sep':'|',
    'encoding':'ISO-8859-1',
    'itens_tabelas_escolas': ItensInfra 
}

def gerarTabelaPontuacao(escolaAno, estado):
    df_escola = pd.read_csv(escolaAno['nome_arquivo_csv'],low_memory=False, encoding=escolaAno['encoding'], sep=escolaAno['sep'])
    df_escola = df_escola[TabelaInfra]
    df_escola = df_escola.fillna(0) #Converte NaN para 0
    if estado != '':
        df_escola = df_escola.loc[(df_escola['ID_DEPENDENCIA_ADM'] < 4) & (df_escola['SIGLA'] == estado) ]
    df_escola = df_escola.copy()
    df_escola["Soma"] = sum( list(map(lambda x,y: x * df_escola[ItensInfra[y]], pesos, sequencia)) )
    df_escola = df_escola[['ANO_CENSO', 'FK_COD_MUNICIPIO', 'Soma']] 
    df_escola["FK_COD_MUNICIPIO"] = df_escola["FK_COD_MUNICIPIO"].astype("double")
    df_escola.rename(columns={'FK_COD_MUNICIPIO':'COD_MUNIC_IBGE'}, inplace=True) # 3) Renomear coluna
    df_escola = df_escola.groupby('COD_MUNIC_IBGE')
    df_escola = df_escola['Soma'].agg([np.sum, np.size])
    df_escola.rename(columns={'sum':'PONTUACAO_ESCOLAS_POR_CIDADE'}, inplace=True)
    df_escola.rename(columns={'size':'QTD_ESCOLAS'}, inplace=True)
    #df_escola.to_csv('df_escola_out.csv',';')
    
    return df_escola
    

