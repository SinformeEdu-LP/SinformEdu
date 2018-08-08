import pandas as pd
import seaborn as sns

pd.set_option("display.max_columns",166)
from IPython import get_ipython
ipy = get_ipython()
if ipy is not None:
    ipy.run_line_magic('matplotlib', 'inline')
    ipy.run_line_magic('pylab', 'inline')
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import geopandas as gpd

def agrupamento2013(x):
    
    result = {
        'ANO_CENSO': x['ANO_CENSO'].min(),
        'NUM_COMP_ALUNOS_POR_CIDADE': x['NUM_COMP_ALUNOS'].sum()
    }
    return pd.Series(result)

def agrupamento2015_2017(x):
    
    result = {
        'ANO_CENSO': x['NU_ANO_CENSO'].min(),
        'NUM_COMP_ALUNOS_POR_CIDADE': x['NU_COMP_ALUNO'].sum()
    }
    return pd.Series(result)

'''def gerarTabelaVariavelEscolas(nomeVariavel, ano): # Gera uma tabela para correlacionar com algum índice
    dfEscolas = pd.read_csv('../arquivos/escolas'+ano+'.csv',low_memory=False, encoding='ISO-8859-1', sep='|')
    dfEscolasAgrupado = dfEscolas.groupby('CO_MUNICIPIO')
    tabela = dfEscolasAgrupado.apply(agrupamento2015_2017)
    #tabela['ANO_CENSO'] = tabela['ANO_CENSO'].apply(int).astype(str)
    #print(tabela)
    print('////////////////////////////////////++++++++++++++++++')
    tabela.to_csv(nomeVariavel+ano+'_out.csv','|')
    return tabela'''

#tabelaEscolas = gerarTabelaVariavelEscolas('numCompPorCidade', '2017')
'''lista_anos = ['2015','2017']
listaTabelasAnos = list(map(lambda x: gerarTabelaVariavelEscolas('numCompPorCidade',x), lista_anos))'''
#print(listaTabelasAnos)

numCompPorMunicipio2015 = pd.read_csv('Dados/numCompPorAlunoPorMunicipio2015_out.csv',low_memory=False, sep='|')
numCompPorMunicipio2017 = pd.read_csv('Dados/numCompPorAlunoPorMunicipio2017_out.csv',low_memory=False, sep='|')

listaTabelasAnos = [numCompPorMunicipio2015, numCompPorMunicipio2017]
tabelaEscolas = pd.concat(listaTabelasAnos)

# IOEB
datasetIOEB_MUNIC = pd.read_csv('Dados/IOEB_2015_2017_MUNIC.csv',low_memory=False, sep=';')
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
datasetIOEB_MUNIC_2015['ANO_CENSO'] = 2015
#print(datasetIOEB_MUNIC_2015)

datasetIOEB_MUNIC_2017 = datasetIOEB_MUNIC.copy()
datasetIOEB_MUNIC_2017 = datasetIOEB_MUNIC_2017[['CO_MUNICIPIO','IOEB17']]
datasetIOEB_MUNIC_2017.rename(columns={'IOEB17':'IOEB'}, inplace=True)
datasetIOEB_MUNIC_2017['ANO_CENSO'] = 2017
#print(datasetIOEB_MUNIC_2017)

datasetIOEB_MUNIC_CONCAT = pd.concat( [datasetIOEB_MUNIC_2015, datasetIOEB_MUNIC_2017] )

#merge 2015 Escolas / IOEB
mergeEscolas_IOEB_2015 = pd.merge(listaTabelasAnos[0], datasetIOEB_MUNIC_2015, how='inner', on=['CO_MUNICIPIO','ANO_CENSO'] )
mergeEscolas_IOEB_2015.to_csv('mergeEscolas_IOEB_2015_2017.csv','|')
corr2015_NumCompu_X_IOEB = mergeEscolas_IOEB_2015['IOEB'].corr(mergeEscolas_IOEB_2015['NUM_COMP_ALUNOS_POR_CIDADE'], method= 'spearman')

#merge 2017 Escolas / IOEB
mergeEscolas_IOEB_2017 = pd.merge(listaTabelasAnos[1], datasetIOEB_MUNIC_2017, how='inner', on=['CO_MUNICIPIO','ANO_CENSO'] )
mergeEscolas_IOEB_2017.to_csv('mergeEscolas_IOEB_2015_2017.csv','|')
corr2017_NumCompu_X_IOEB = mergeEscolas_IOEB_2017['IOEB'].corr(mergeEscolas_IOEB_2017['NUM_COMP_ALUNOS_POR_CIDADE'], method= 'spearman')

#merge 2015_2017 Escolas / IOEB
mergeEscolas_IOEB = pd.merge(tabelaEscolas, datasetIOEB_MUNIC_CONCAT, how='inner', on=['CO_MUNICIPIO','ANO_CENSO'] )
mergeEscolas_IOEB.to_csv('mergeEscolas_IOEB_2015_2017.csv','|')
corr2015_2017_NumCompu_X_IOEB = mergeEscolas_IOEB['IOEB'].corr(mergeEscolas_IOEB['NUM_COMP_ALUNOS_POR_CIDADE'], method= 'spearman')

listCorrNumCompu_X_IOEB = [corr2015_NumCompu_X_IOEB, corr2017_NumCompu_X_IOEB, corr2015_2017_NumCompu_X_IOEB]

X = list(range(1,4))

listAnos = ['2015','2017','2015-2017']

print(listCorrNumCompu_X_IOEB)

data = pd.DataFrame({'A': listAnos,
                    'B': listCorrNumCompu_X_IOEB})

data.plot.bar(x='A', y='B', rot=0)
#data.plot(figsize=(4, 15),kind='barh', title='Proposta para Pernambuco')
plt.xlabel('Anos')
plt.ylabel('Correlação')
plt.savefig(r'GraficoCorr_NumCompXIOEB.png')



