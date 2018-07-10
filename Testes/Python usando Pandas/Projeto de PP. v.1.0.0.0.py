# coding: utf-8

#importação
import pandas as pd
import seaborn as sns
pd.set_option("display.max_columns",166)
get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('pylab', 'inline')
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import geopandas as gpd

#importação arquivo
datasetMPont = pd.read_csv(r'C:\Users\wellington\Documents\ciencia dos dados\dados\pontuacaoMunic.csv', sep=';')
datasetProposta = pd.read_csv(r'C:\Users\wellington\Documents\ciencia dos dados\dados\siconv_proposta.csv', sep=';')
datasetEmenda = pd.read_csv(r'C:\Users\wellington\Documents\ciencia dos dados\dados\siconv_emenda.csv', sep=';')
datasetEscola2013 = pd.read_csv(r'C:\Users\wellington\Documents\ciencia dos dados\dados\escolas2013.csv',low_memory=False, encoding='ISO-8859-1', sep='|')
municipios = pd.read_csv(r'C:\Users\wellington\Documents\ciencia dos dados\dados\municipios.csv',low_memory=False, encoding='ISO-8859-1', sep=';')
mapaDigital = gpd.read_file(r'C:\Users\wellington\Documents\ciencia dos dados\dados\26MUE250GC_SIR.shp')

#função de geração de gráficos
def proposta():
    prospostaEducacao = datasetProposta.loc[(datasetProposta['DESC_ORGAO_SUP'] == 'MINISTERIO DA EDUCACAO')]
    return prospostaEducacao

def pontuacaoEstado():
    pontuacaoMunicipios = municipios['NM_UF'].value_counts()
    pontuacaoMunicipios.plot(figsize=(15, 15),kind='barh', title='Pontuação dos Estados')
    plt.xlabel('Pontuação')
    plt.ylabel('Estado')
    plt.savefig('PontuacaodosEstados.png')
    #plt.show()
   
def situacaoProspostas():
    prospostaEducacao = proposta()  
    prospostaEducacao = prospostaEducacao['SITUACAO_CONTA'].value_counts()
    prospostaEducacao.plot(figsize=(10, 4),kind= 'barh', title='Situacao das Prospostas')
    plt.xlabel('Quantidade')
    plt.ylabel('Situação')
    plt.savefig(r'gráficos\SituacaoProjetoBasico.png')
    #plt.show()

def situaçãoProjetoBasico():
    prospostaEducacao = proposta()  
    prospostaEducacao = prospostaEducacao['SITUACAO_PROJETO_BASICO'].value_counts().plot(figsize=(15, 6),kind= 'barh', title='Situacao do Projeto Básico')
    plt.xlabel('Quantidade')
    plt.ylabel('Situação')
    plt.savefig(r'gráficos\Naturezadaproposta.png')
    #plt.show()

def naturezaProposta(): 
    prospostaEducacao = proposta()  
    prospostaEducacao = prospostaEducacao['NATUREZA_JURIDICA'].value_counts().plot(figsize=(10, 4),kind= 'barh', title='Natureza da proposta')
    plt.xlabel('Natureza')
    plt.ylabel('Quantidade')
    plt.savefig('Naturezadaproposta.png')
    #plt.show()     

def unidadeProponente():
    prospostaEducacao = proposta()    
    prospostaEducacao= prospostaEducacao['UF_PROPONENTE'].value_counts().plot(figsize=(15, 4),kind='bar', title='Propostas por Estado')
    plt.xlabel("Estado")
    plt.ylabel('Propostas')
    plt.savefig(r'UnidadeProponente.png')
    #plt.show()
    
def unidadeProponentePernambuco():
    prospostaEducacao = proposta()  
    prospostaEducacaoPE=prospostaEducacao.loc[(prospostaEducacao['UF_PROPONENTE'] == 'PE')].groupby('UF_PROPONENTE')[u'MUNIC_PROPONENTE'].value_counts()
    prospostaEducacaoPE.plot(figsize=(15, 4),kind='barh', title='Proposta para Pernambuco')
    plt.xlabel('Quantidade de Propostas')
    plt.ylabel('Cidades')
    plt.savefig(r'UnidadeProponente(Pernambuco).png')
    #plt.show()
    
def tipoEmendas():
    emendas = (datasetEmenda['TIPO_PARLAMENTAR']).value_counts().plot(figsize=(8, 2),kind='barh', title='Tipo de Emendas' )
    plt.xlabel("Quantidade")
    plt.ylabel('Tipo')
    plt.savefig('TipodeEmendas.png')
    #plt.show()

def mapaPontuacaoPE():                  
    mapaDigitalDt = pd.DataFrame(mapaDigital)
    datasetMPont.drop_duplicates(inplace=True)
    datasetMPont['CD_GEOCMU'] = datasetMPont['COD_MUNIC_IBGE'].apply(int)
    mapaDigitalDt['CD_GEOCMU'] =  mapaDigitalDt['CD_GEOCMU'].apply(int)
    mapa  = pd.merge(mapaDigitalDt, datasetMPont, how = 'inner')

    mapa = gpd.GeoDataFrame(mapa)
    mapa.plot(column='PONTUACAO_ESCOLAS_POR_CIDADE', cmap = 'RdYlGn_r', )

    plt.xlabel('Pontuação das cidades')
    plt.savefig('UnidadeProponente.png')
    #plt.show()

def main():
    pontuacaoEstado()
    situacaoProspostas()
    situaçãoProjetoBasico()
    naturezaProposta()
    unidadeProponente()
    unidadeProponentePernambuco()
    tipoEmendas()
    mapaPontuacaoPE()

main()
