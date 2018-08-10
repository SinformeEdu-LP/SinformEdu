import pandas as pd

pd.set_option("display.max_columns",166)
from IPython import get_ipython
ipy = get_ipython()
if ipy is not None:
    ipy.run_line_magic('matplotlib', 'inline')
    ipy.run_line_magic('pylab', 'inline')
import matplotlib.pyplot as plt
plt.style.use('ggplot')

itensPorMunicipio2015 = pd.read_csv('correlacao/itens_Por_Municipio2015_out.csv',low_memory=False, sep='|')
itensPorMunicipio2017 = pd.read_csv('correlacao/itens_Por_Municipio2017_out.csv',low_memory=False, sep='|')

listaItensEscolasPorMunicipio = [itensPorMunicipio2015, itensPorMunicipio2017]
tabelaItensEscolasPorMunic = pd.concat(listaItensEscolasPorMunicipio)

print(tabelaItensEscolasPorMunic.head(1))

# IOEB
datasetIOEB_MUNIC = pd.read_csv('correlacao//IOEB_2015_2017_MUNIC.csv',low_memory=False, sep=';')
datasetIOEB_MUNIC = datasetIOEB_MUNIC[['cod_munic','IOEB15', 'IOEB17']]
datasetIOEB_MUNIC['IOEB15'] = datasetIOEB_MUNIC['IOEB15'].str.replace(',','.')
datasetIOEB_MUNIC['IOEB15'] = datasetIOEB_MUNIC['IOEB15'].apply(float)

datasetIOEB_MUNIC['IOEB17'] = datasetIOEB_MUNIC['IOEB17'].str.replace(',','.')
datasetIOEB_MUNIC['IOEB17'] = datasetIOEB_MUNIC['IOEB17'].apply(float)
datasetIOEB_MUNIC = datasetIOEB_MUNIC.fillna(0) #Converte NaN para 0
datasetIOEB_MUNIC.rename(columns={'cod_munic':'CO_MUNICIPIO'}, inplace=True)

datasetIOEB_MUNIC_2015 = datasetIOEB_MUNIC.copy()
datasetIOEB_MUNIC_2015 = datasetIOEB_MUNIC_2015[['CO_MUNICIPIO','IOEB15']]
datasetIOEB_MUNIC_2015.rename(columns={'IOEB15':'IOEB'}, inplace=True)
datasetIOEB_MUNIC_2015['NU_ANO_CENSO'] = 2015
#print(datasetIOEB_MUNIC_2015)

datasetIOEB_MUNIC_2017 = datasetIOEB_MUNIC.copy()
datasetIOEB_MUNIC_2017 = datasetIOEB_MUNIC_2017[['CO_MUNICIPIO','IOEB17']]
datasetIOEB_MUNIC_2017.rename(columns={'IOEB17':'IOEB'}, inplace=True)
datasetIOEB_MUNIC_2017['NU_ANO_CENSO'] = 2017
#print(datasetIOEB_MUNIC_2017)

datasetIOEB_MUNIC_CONCAT = pd.concat( [datasetIOEB_MUNIC_2015, datasetIOEB_MUNIC_2017] )

def correlacaoTabelas(tabela, item):
    correlacao = tabela['IOEB'].corr(tabela[item], method= 'spearman')
    return correlacao

def gerarlistaCorrelacoes(tabela1, tabela2, listaItens):
    mergeTabelas = pd.merge(tabela1, tabela2, how='inner', on=['CO_MUNICIPIO','NU_ANO_CENSO'] )
    mergeTabelas.to_csv('mergeEscolas_IOEB_2015_2017.csv','|')
    listaCorrItens = list(map(lambda x: correlacaoTabelas(mergeTabelas, x), listaItens))
    return listaCorrItens

listItens2015_2017 = ['COMP_POR_ALUNO(%)','MEDIA_QTD_ALUNOS_POR_ESCOLA','NUM_ESCOLAS_INTERNET_MUNIC','MEDIA_SALAS_EXISTENTES','MEDIA_PONTUACAO']

listaCorrelacoesIOEB = gerarlistaCorrelacoes(tabelaItensEscolasPorMunic, datasetIOEB_MUNIC_CONCAT, listItens2015_2017)
print(listaCorrelacoesIOEB)




