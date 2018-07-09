import pandas as pd
datasetProposta = pd.read_csv('~/Documentos/Pandas Testes/siconv_proposta.csv', sep=';')
print(datasetProposta.columns)
print()
dtPE = datasetProposta.loc[datasetProposta['VL_CONTRAPARTIDA_PROP'] == 40000]

listaColunas = []
selectColunas = [0,1,3]
for i in selectColunas:
    listaColunas.append(datasetProposta.columns[i])

dp = datasetProposta[listaColunas]
print(dp)

dpp = dp.copy() 

dpp["Soma"] = dp.sum(axis=1)

print()
print(dpp)

