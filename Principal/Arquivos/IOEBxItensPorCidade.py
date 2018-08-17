import pandas as pd
import numpy as np

maximoColunasMostradas = 170
pd.set_option("display.max_columns",maximoColunasMostradas)
from IPython import get_ipython
ipy = get_ipython()
if ipy is not None:
    ipy.run_line_magic('matplotlib', 'inline')
    ipy.run_line_magic('pylab', 'inline')
import matplotlib.pyplot as plt
plt.style.use('ggplot')

import plotly
plotly.tools.set_credentials_file(username='user', api_key='code') # Usuario e senha retirados
import plotly.plotly as py
import plotly.graph_objs as go

def separarTabelaIOEB(tabela, ano):
    nomeColuna = 'IOEB'+ ano[2:]
    tabela[nomeColuna] = tabela[nomeColuna].str.replace(',','.')
    tabela[nomeColuna] = tabela[nomeColuna].apply(float)
    tabela = tabela.fillna(0) #Converte NaN para 0
    tabela.rename(columns={'cod_munic':'CO_MUNICIPIO'}, inplace=True)
    tabela = tabela.copy()
    tabela = tabela[['CO_MUNICIPIO', nomeColuna]]
    tabela.rename(columns={nomeColuna:'IOEB'}, inplace=True)
    tabela['NU_ANO_CENSO'] = int(ano)
    return tabela

def gerarListaTabelas(tabela, listaAnos):
    listaTabelas = list(map(lambda x: separarTabelaIOEB(tabela, x), listaAnos))
    return listaTabelas

def correlacaoTabelas(tabela, item):
    correlacao = tabela['IOEB'].corr(tabela[item], method= 'spearman')
    return correlacao

def gerarlistaCorrelacoes(tabela1, tabela2, listaItens):
    mergeTabelas = pd.merge(tabela1, tabela2, how='inner', on=['CO_MUNICIPIO','NU_ANO_CENSO'] )
    listaCorrItens = list(map(lambda x: correlacaoTabelas(mergeTabelas, x), listaItens))
    return listaCorrItens

def concatenarTabelasItensEscolas():
    itensPorMunicipio2015 = pd.read_csv('../Dados/Correlacao/itens_Por_Municipio2015_out.csv',low_memory=False, sep='|')
    itensPorMunicipio2017 = pd.read_csv('../Dados/Correlacao/itens_Por_Municipio2017_out.csv',low_memory=False, sep='|')
    tabelaItensEscolas = pd.concat([itensPorMunicipio2015, itensPorMunicipio2017])
    return tabelaItensEscolas

def concatenarTabelasIOEB():
    datasetIOEB_MUNIC = pd.read_csv('../Dados/Correlacao/IOEB_2015_2017_MUNIC.csv',low_memory=False, sep=';')
    datasetIOEB_MUNIC = datasetIOEB_MUNIC[['cod_munic','IOEB15', 'IOEB17']]
    listaAnos = ['2015','2017']
    tabelasIOEB = gerarListaTabelas(datasetIOEB_MUNIC, listaAnos)
    datasetIOEB_MUNIC = pd.concat( tabelasIOEB )
    return datasetIOEB_MUNIC

def gerarGraficosCorrelacesItensXIOEB():

    tabelaItensEscolasPorMunic = concatenarTabelasItensEscolas()
    datasetIOEB_MUNIC_CONCAT = concatenarTabelasIOEB()
    listItens2015_2017 = ['COMP_POR_ALUNO(%)','MEDIA_QTD_ALUNOS_POR_ESCOLA','NUM_ESCOLAS_INTERNET_MUNIC','MEDIA_SALAS_EXISTENTES','MEDIA_PONTUACAO']
    listaValoresCorrelacoesIOEB = gerarlistaCorrelacoes(tabelaItensEscolasPorMunic, datasetIOEB_MUNIC_CONCAT, listItens2015_2017)
    
    data = pd.DataFrame({'A': listItens2015_2017,
                        'B': listaValoresCorrelacoesIOEB})
    
    data.plot.bar(x='A', y='B', rot=90)
    plt.title('Correlação do Itens das Escolas X IOEB')
    plt.xlabel('Itens')
    plt.ylabel('Correlação')
    plt.savefig('../Resultados/Graficos/correlacoesItensEscolasxIOEB.png')
    plt.show()
       
    #O gráfico é gerado com a biblioteca plotly, que exige senha para gerar os gráficos
    #Então foi criada uma conta, o grafico foi gerado, e em seguida o user e key foram retirados do código
    #para não deixar público
    '''data = [go.Bar(
                x=listItens2015_2017,
                y=listaCorrelacoesIOEB
        )]
    
    py.iplot(data, filename='correlacoesItensEscolasxIOEB')'''


#gerarGraficosCorrelacesItensXIOEB()


