import pandas as pd

pd.set_option("display.max_columns",166)
from IPython import get_ipython
ipy = get_ipython()
if ipy is not None:
    ipy.run_line_magic('matplotlib', 'inline')
    ipy.run_line_magic('pylab', 'inline')
import matplotlib.pyplot as plt
plt.style.use('ggplot')

import plotly
plotly.tools.set_credentials_file(username='user', api_key='code')
import plotly.plotly as py
import plotly.graph_objs as go

itensPorMunicipio2015 = pd.read_csv('../Dados/Correlacao/itens_Por_Municipio2015_out.csv',low_memory=False, sep='|')
itensPorMunicipio2017 = pd.read_csv('../Dados/Correlacao/itens_Por_Municipio2017_out.csv',low_memory=False, sep='|')

listaItensEscolasPorMunicipio = [itensPorMunicipio2015, itensPorMunicipio2017]
tabelaItensEscolasPorMunic = pd.concat(listaItensEscolasPorMunicipio)

print(tabelaItensEscolasPorMunic.head(1))

# IOEB
datasetIOEB_MUNIC = pd.read_csv('../Dados/Correlacao/IOEB_2015_2017_MUNIC.csv',low_memory=False, sep=';')
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

data = pd.DataFrame({'A': listItens2015_2017,
                    'B': listaCorrelacoesIOEB})

data.plot.bar(x='A', y='B', rot=0)
#data.plot(figsize=(4, 15),kind='barh', title='Proposta para Pernambuco')
plt.xlabel('Anos')
plt.ylabel('Correlação')
plt.savefig(r'../Resultados/Graficos/correlacoesItensEscolasxIOEB.png')

data = [go.Bar(
            x=listItens2015_2017,
            y=listaCorrelacoesIOEB
    )]

py.iplot(data, filename='correlacoesItensEscolasxIOEB')




