
# coding: utf-8

# In[1]:


#imports
import pandas as pd
import seaborn as sns
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
# plt.style.use('ggplot')
import geopandas as gpd
import glob
pd.set_option("display.max_columns",166)
get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('pylab', 'inline')


def encontrarArquivo(arq): 
     #trocar pelo caminho absoluto onde está os arquivos no seu computador 
    caminhoPasta = r'C:\Users\wellington\Documents\ciencia dos dados\dados'
    
    #encontra o caminho
    caminho = (caminhoPasta +"/"+ arq)
    return caminho

datasetMPont = pd.read_csv(encontrarArquivo("pontuacaoMunic.csv"), sep=';')


datasetProposta = pd.read_csv(encontrarArquivo('siconv_proposta.csv'), sep=';')
propostaEducacao = datasetProposta.loc[(datasetProposta['DESC_ORGAO_SUP'] == 'MINISTERIO DA EDUCACAO')]
# propostaEducacao.to_csv(r"propostasEducacao.csv", ";")

datasetEmenda = pd.read_csv(encontrarArquivo('siconv_emenda.csv'), sep=';')
datasetEmpenho = pd.read_csv(encontrarArquivo('siconv_empenho.csv'), sep=';')
datasetHistSitua = pd.read_csv(encontrarArquivo('siconv_historico_situacao.csv'), sep=';')
datasetEscola2013 = pd.read_csv(encontrarArquivo('escolas2013.csv'),low_memory=False, encoding='ISO-8859-1', sep='|')

def agrupamento1(x):
        result = {'CD_GEOCUF': x['FK_COD_ESTADO'].min(), 'UF': x['SIGLA'].min()}
        return pd.Series(result)
    
def agrupamento2(x):
    result = { 'cont': x['UF'].count(), 'CD_GEOCUF': x['CD_GEOCUF'].min(), 'UF': x['UF'].min(), 'Partido': x['Partido'].count()}
    return pd.Series(result)

def emendasPartidos(propostaEmendasEducacao):
    # Gera gráfico emendas por partidos
    propostaEmendasEducacao ["Partido"].value_counts().plot(kind="barh")
    plt.ylabel('Emendas de Educação por Partido')
    plt.xlabel('Quantidade de Emendas de Educação por Partido')
    plt.savefig(r'emendaPartidpsbarra.png')

def emendasEstado(propostaEmendasEducacao):
    # Gera gráfico emendas por Estados
    propostaEmendasEducacao ["UF"].value_counts().plot(kind="barh")
    plt.ylabel('Emendas de Educação por Estado')
    plt.xlabel('Quantidade de Emendas de Educação por Estado')
    plt.savefig(r'emendaEstadosbarra.png')
    
def emendasEstadoGraficoCaixa(propostaEmendasEducacao):
    # Gera gráfico emendas por partidos
    propostaEmendasEducacao["UF"].value_counts().plot(kind="box")
    plt.savefig(r'emendaEstadoscaixa.png')
    return 
   

def mapaPontuacaoBR(propostaEducacao):                  
    mapaDigital = gpd.read_file(encontrarArquivo('BRUFE250GC_SIR.shp'))
    mapaDigitalDt = pd.DataFrame(mapaDigital)
    
    propostaEducacao.drop_duplicates(inplace=True)
    mapaDigitalDt['CD_GEOCUF'] =  mapaDigitalDt['CD_GEOCUF'].apply(int)
    mapaAnt = pd.merge(propostaEducacao, mapaDigitalDt, on='CD_GEOCUF', how = 'inner') 
    mapa = gpd.GeoDataFrame(mapaAnt)

    mapa.plot(column = "Partido", cmap = 'vlag_r')
    red_patch = mpatches.Patch(color='crimson', label='Mais Emenda')
    plt.legend(handles=[red_patch])
    plt.xlabel('Emendas de Educação por Estado')
    plt.savefig(r'emendaEstado.png')
    plt.show()  

def propostaEmendasEducacao():
    estados = datasetEscola2013 
    # .to_csv('MergeEmendasPropostas.csv',';')
    estados = estados[['FK_COD_ESTADO', 'SIGLA']]

    estados = estados.groupby('SIGLA').apply(agrupamento1)

    propostaParl = pd.merge(datasetProposta, datasetEmenda, on = 'ID_PROPOSTA', how ='inner')

    propostaEducacao = propostaParl.loc[(propostaParl['DESC_ORGAO_SUP'] == 'MINISTERIO DA EDUCACAO')]

    datasetdep_senador = pd.read_csv(encontrarArquivo('dep_senad.csv'), sep=",")
    datasetdep_senador.rename(columns={'Nome Civil':'NOME_PARLAMENTAR'}, inplace=True)
    datasetdep_senador
    propostaEducacao = pd.merge(propostaEducacao, datasetdep_senador, on ='NOME_PARLAMENTAR', how= 'inner')
    estados.rename(columns={'SIGLA':'UF'}, inplace=True)
    propostaEmendasEducacao = pd.merge(propostaEducacao, estados, on = "UF", how = "inner" )
    
    emendasPartidos(propostaEmendasEducacao)   
    emendasEstado(propostaEmendasEducacao)
    emendasEstadoGraficoCaixa(propostaEmendasEducacao)

    mapaPontuacaoBR(propostaEmendasEducacao)

propostaEmendasEducacao()

