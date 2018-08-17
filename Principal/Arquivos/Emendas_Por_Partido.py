# coding: utf-8

#imports
import pandas as pd
maximoColunasMostradas = 170 
pd.set_option("display.max_columns",maximoColunasMostradas)
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import matplotlib.patches as mpatches
import glob
from IPython import get_ipython
ipy = get_ipython()
if ipy is not None:
    ipy.run_line_magic('matplotlib', 'inline')
    ipy.run_line_magic('pylab', 'inline')
import geopandas as gpd
import collections

def encontrarArquivo(arq): 
    #trocar pelo caminho absoluto onde está os arquivos no seu computador 
    caminhoPasta = './Dados'
    #encontra o caminho
    caminho = (caminhoPasta +"/"+ arq)
    return caminho

def emendasEstadoGraficoCaixa(propostaEmendasEducacao):
    # Gera gráfico emendas por partidos
    plt.title('Quantidade de Emendas de Educação por Partido')
    propostaEmendasEducacao["UF"].value_counts().plot(kind="box")
    plt.savefig('./Resultados/Graficos/QtdEmendasPorPartido_Caixa.png')

def emendasPartidos(propostaEmendasEducacao):
    # Gera gráfico emendas por partidos
    propostaEmendasEducacao ["Partido"].value_counts().plot(kind="barh")
    plt.title('Quantidade de Emendas de Educação por Partido')
    plt.ylabel('Partido')
    plt.xlabel('Quantidade de Emendas de Educação')
    plt.savefig('./Resultados/Graficos/QtdEmendasPorPartido_Barra.png')

def mapaPontuacaoBR(propostaEducacao):                  
    mapaDigital = gpd.read_file(encontrarArquivo('Shapefiles/BR-UF/BRUFE250GC_SIR.shp'))
    mapaDigitalDt = pd.DataFrame(mapaDigital)
    propostaEducacao.drop_duplicates(inplace=True)
    mapaDigitalDt['CD_GEOCUF'] =  mapaDigitalDt['CD_GEOCUF'].apply(int)
    mapaAnt = pd.merge(propostaEducacao, mapaDigitalDt, on='CD_GEOCUF', how = 'inner') 
    mapa = gpd.GeoDataFrame(mapaAnt)
    mapa.plot(column = "Partido", cmap = 'RdYlGn')
    red_patch = mpatches.Patch(color='#910000', label='Menos Emendas')
    green_patch = mpatches.Patch(color='#397800', label='Mais Emendas')
    plt.legend(handles=[green_patch, red_patch])
    plt.title('Quantidade de Emendas de Educação por Estado')
    plt.savefig('./Resultados/Graficos/QtdEmendaPorEstadoMapa.png')
    plt.show()

# Emendas de Educação por partido
def agrupamento1(x):
    result = {'CD_GEOCUF': x['FK_COD_ESTADO'].min(), 
              'UF': x['SIGLA'].min()}
    return pd.Series(result)
    
def agrupamento2(x):
    result = { 'cont': x['UF'].count(), 
              'CD_GEOCUF': x['CD_GEOCUF'].min(), 
              'UF': x['UF'].min(), 
              'Partido': x['Partido'].count()}
    
    return pd.Series(result)

def propostaEmendasEducacao(datasetProposta, datasetEmenda, datasetEscola2013):
    estados = datasetEscola2013 
    estados = estados[['FK_COD_ESTADO', 'SIGLA']]
    estados = estados.groupby('SIGLA').apply(agrupamento1)
    propostaParl = pd.merge(datasetProposta, datasetEmenda, on = 'ID_PROPOSTA', how ='inner')
    propostaEducacao = propostaParl.loc[(propostaParl['DESC_ORGAO_SUP'] == 'MINISTERIO DA EDUCACAO')]
    datasetdep_senador = pd.read_csv(encontrarArquivo('deputados.csv'), sep=";")
    datasetdep_senador.rename(columns={'Nome sem Acento':'NOME_PARLAMENTAR'}, inplace=True)
    propostaEducacao = pd.merge(propostaEducacao, datasetdep_senador, on ='NOME_PARLAMENTAR', how= 'inner')
    estados.rename(columns={'SIGLA':'UF'}, inplace=True)
    propostaEmendasEducacao = pd.merge(propostaEducacao, estados, on = "UF", how = "inner" )
    emendasPartidos(propostaEmendasEducacao)
    mapaPontuacaoBR(propostaEmendasEducacao)
    emendasEstadoGraficoCaixa(propostaEmendasEducacao)
    
def gerarGraficosEmendaPorPartido():
    datasetProposta = pd.read_csv(encontrarArquivo('siconv_proposta.csv'), sep=';')
    datasetEmenda = pd.read_csv(encontrarArquivo('siconv_emenda.csv'), sep=';')
    datasetEscola2013 = pd.read_csv(encontrarArquivo('escolas2013.csv'),low_memory=False, encoding='ISO-8859-1', sep='|')       
    propostaEmendasEducacao(datasetProposta, datasetEmenda, datasetEscola2013)

#gerarGraficosEmendaPorPartido()

