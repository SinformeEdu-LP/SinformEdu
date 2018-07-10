import pandas as pd
import numpy as np

datasetProposta = pd.read_csv('~/Documentos/Pandas Testes/siconv_proposta.csv',low_memory=False, sep=';')
print("datasetProposta - Colunas: ")
#print(datasetProposta.columns)
print()

prospostaEducacaoPE = datasetProposta.loc[(datasetProposta['DESC_ORGAO_SUP'] == 'MINISTERIO DA EDUCACAO') & (datasetProposta['UF_PROPONENTE'] == 'PE')]
print("prospostaEducacaoPE - Colunas: ")
#print(prospostaEducacaoPE.columns)
print()

listaColunasProp = []
selectColunasProp = [3,2,28]
listaColunasProp = list(map(lambda x: prospostaEducacaoPE.columns[x], selectColunasProp))

prospostaEducacaoPE = prospostaEducacaoPE[listaColunasProp]

# Passar para numero
prospostaEducacaoPE['VL_REPASSE_PROP'] = prospostaEducacaoPE['VL_REPASSE_PROP'].str.replace(',','.')
prospostaEducacaoPE["VL_REPASSE_PROP"] = prospostaEducacaoPE["VL_REPASSE_PROP"].astype("double") # 1) Passar uma coluna para double, int, float
print(prospostaEducacaoPE) 

reeProp = prospostaEducacaoPE.groupby('COD_MUNIC_IBGE')
finalProp = reeProp['VL_REPASSE_PROP'].agg([np.sum, np.size])

print("**********************++++++++++**********")

#finalProp.columns = ['COD_MUNIC_IBGE','MUNIC_PROPONENTE','SOMA_VALOR_REPASSE_POR_CIDADE','QTD_PROPOSTAS']
finalProp.rename(columns={'sum':'SOMA_VALOR_REPASSE_POR_CIDADE'}, inplace=True)
finalProp.rename(columns={'size':'QTD_PROPOSTAS'}, inplace=True)
print(finalProp)
finalProp.to_csv('finalProp_out.csv',';')
print()

''' ESCOLAS '''

datasetEscola2010 = pd.read_csv('~/Documentos/Pandas Testes/escolas2010.csv',low_memory=False, sep='|')
print("datasetEscola2010 - Colunas: ")
#print(datasetEscola2010.columns)
print()

datasetEscola2013 = pd.read_csv('~/Documentos/Pandas Testes/escolas2013.csv',low_memory=False, encoding='ISO-8859-1', sep='|')
print("datasetEscola2013 - Públicas - Colunas: ")
#print(datasetEscola2013.columns)
print()
dtEscolaPublicaPE = datasetEscola2013.loc[(datasetEscola2013['ID_DEPENDENCIA_ADM'] < 4) & (datasetEscola2013['SIGLA'] == 'PE') ]

listaColunas = []
selectColunas = [0,9,32,53,59,94,95,97,98]
#selectColunas = [0,32,53]

listaColunas = list(map(lambda x: dtEscolaPublicaPE.columns[x], selectColunas))

dtInfra = dtEscolaPublicaPE[listaColunas]
#print(dtInfra)
dtInfra = dtInfra.fillna(0) #Converte NaN para 0
print("*********************************************")
#print(dtInfra)
dtInfra.to_csv('dtInfra_out.csv',';')
#print(dtInfra.columns)
print()

dtInfra2 = dtInfra.copy()

pesos = [10,30,25,30,5,20,10]
#pesos = [10,30]
#sequencia = [1,2]
sequencia = [2,3,4,5,6,7,8]

#pontosColunas = list(map(lambda x,y: x * y, pesos, selectColunas))

#dtInfra2["Soma"] = dtInfra.sum(axis=1)
#dtInfra2["Soma"] = 10 * dtInfra[listaColunas[1]] + 20 * dtInfra[listaColunas[2]]
dtInfra2["Soma"] = sum( list(map(lambda x,y: x * dtInfra[listaColunas[y]], pesos, sequencia)) )

print()
#print(dtInfra2)
dtInfra2.to_csv('dtInfra2_out.csv',';')
#print(dtInfra2.columns)
print()

print()
print("Soma Total", dtInfra2["Soma"].sum())

resultado = dtInfra2[['ANO_CENSO', 'FK_COD_MUNICIPIO', 'Soma']]
'''resultadoPE = resultado.loc[(resultado['FK_COD_MUNICIPIO'] == 3549904)]
print(resultadoPE)'''
print()

resultado = resultado.copy()
resultado["FK_COD_MUNICIPIO"] = resultado["FK_COD_MUNICIPIO"].astype("double")
resultado.rename(columns={'FK_COD_MUNICIPIO':'COD_MUNIC_IBGE'}, inplace=True) # 3) Renomear coluna

ree = resultado.groupby('COD_MUNIC_IBGE')
final = ree['Soma'].agg([np.sum, np.size])
final.rename(columns={'sum':'PONTUACAO_ESCOLAS_POR_CIDADE'}, inplace=True)
final.rename(columns={'size':'QTD_ESCOLAS'}, inplace=True)

final.to_csv('final_out.csv',';')
print("*********************************************")
print(final.columns)
print("---------------------***Final**----------------------------")
print(final)
#final.columns = ['COD_MUNIC_IBGE','PONTUACAO_ESCOLAS','QTD_ESCOLAS']

'''concat = pd.DataFrame.merge(finalProp, final,
                         on=['COD_MUNIC_IBGE'],
                         how='inner')
print("------------Concat---------------------------------")
print(concat)
concat.to_csv('concat_out.csv',';')'''

concat2 = pd.merge(final, finalProp,  how='left', on='COD_MUNIC_IBGE')
print("------------Concat2---------------------------------")
print(concat2)
concat2.to_csv('concat2_out.csv',';')

'''concat3 = final.join(finalProp.set_index('COD_MUNIC_IBGE'), on='COD_MUNIC_IBGE')
#concat3 = final.set_index('COD_MUNIC_IBGE').join(finalProp.set_index('COD_MUNIC_IBGE'))
print("------------Concat3---------------------------------")
print(concat3)
concat3.to_csv('concat3_out.csv',';')'''

datasetMunicipios = pd.read_csv('~/Documentos/Pandas Testes/municipios.csv',low_memory=False, encoding='ISO-8859-1', sep=';')
print("Municipios - Colunas: **************")
print(datasetMunicipios.columns) # ID;CD_GCUF;NM_UF;NM_UF_SIGLA;CD_GCMUN;NM_MUN_2017;AR_MUN_2017
print()
datasetMunicipios.rename(columns={'CD_GCMUN':'COD_MUNIC_IBGE'}, inplace=True)
print(datasetMunicipios.columns)
#print(datasetMunicipios)

concat4 = pd.merge(concat2, datasetMunicipios,  how='left', on='COD_MUNIC_IBGE')
print("------------Concat4---------------------------------")

#AR_MUN_2017 suubstituir , por ponto
concat4['AR_MUN_2017'] = concat4['AR_MUN_2017'].str.replace(',','.')
concat4['AR_MUN_2017'] = concat4['AR_MUN_2017'].astype("double")
print(concat4)
concat4.to_csv('concat4_out.csv',';')







