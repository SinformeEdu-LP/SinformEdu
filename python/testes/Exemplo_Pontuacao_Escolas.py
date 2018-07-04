import pandas as pd 
datasetEscola2010 = pd.read_csv('~/Documentos/Pandas Testes/escolas2010.csv', sep='|')
print("datasetEscola2010 - Colunas: ")
print(datasetEscola2010.columns)
print()

datasetEscola2013 = pd.read_csv('~/Documentos/Pandas Testes/escolas2013.csv', sep='|')

dtEscolaPublica = datasetEscola2013.loc[datasetEscola2013['ID_DEPENDENCIA_ADM'] < 4]
print("datasetEscola2013 - Públicas - Colunas: ")
print(dtEscolaPublica.columns)
print()

listaColunas = []
selectColunas = [0,1,3]

listaColunas = list(map(lambda x: dtEscolaPublica.columns[x], selectColunas))

dtInfra = dtEscolaPublica[listaColunas]
print(dtInfra)

dtInfra2 = dtInfra.copy() 

dtInfra2["Soma"] = dtInfra.sum(axis=1)
'''dpp["Soma"] = peso0 * dp[listaColunas[0]] + peso1 * dp[listaColunas[1]]'''

print()
print(dtInfra2)

print()
print("Soma Total", dtInfra2["Soma"].sum())

