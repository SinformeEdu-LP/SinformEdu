# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd


datasetEscola2010 = pd.read_csv(r'C:\Users\silli\OneDrive\Documentos\GitHub\SinformEdu\arquivos\escolas2010.csv',low_memory=False, encoding='ISO-8859-1', sep='|')
datasetEscola2013 = pd.read_csv(r'C:\Users\silli\OneDrive\Documentos\GitHub\SinformEdu\arquivos\escolas2013.csv',low_memory=False, encoding='ISO-8859-1', sep='|')
mapaPE = gpd.read_file(r'C:\Users\silli\OneDrive\Documentos\GitHub\SinformEdu\arquivos\Shapes\PE\26MUE250GC_SIR.shp')

# Cria um dataset com uma coluna com todos os c�digos do municipios e outra coluna Somando a quantidade de computadores
# de todas as escolas daquele municipio de acordo com o Ano
# ----------------------------------------------------------------------------------------------------------------------------------------#
def escolasMunicipioPE2010():
    dtEscolaPublica2010 = datasetEscola2010.loc[(datasetEscola2010['ID_DEPENDENCIA_ADM'] < 4 ) & (datasetEscola2010['SIGLA'] == "PE" )]
    dtEscolaPublica2010 = dtEscolaPublica2010[['NUM_COMPUTADORES','FK_COD_MUNICIPIO']]
    dtEscolaPublica2010.columns = ['Comp_2010','municipio']
    dtEscolaPublica2010 = dtEscolaPublica2010.groupby(['municipio']).Comp_2010.sum().to_frame()
    return dtEscolaPublica2010
def escolasMunicipioPE2013():
    dtEscolaPublica2013 = datasetEscola2013.loc[(datasetEscola2013['ID_DEPENDENCIA_ADM'] == 3 ) & (datasetEscola2013['SIGLA'] == "PE" )]
    dtEscolaPublica2013 = dtEscolaPublica2013[['NUM_COMPUTADORES','FK_COD_MUNICIPIO']]
    dtEscolaPublica2013.columns = ['Comp_2013','municipio']
    dtEscolaPublica2013 = dtEscolaPublica2013.groupby(['municipio']).Comp_2013.sum().to_frame()
    return dtEscolaPublica2013
# ----------------------------------------------------------------------------------------------------------------------------------------#
#Concatena através do Merge O resultado dos metódos anteriores, criando um dataframe com 3 colunas(Municipio, Comp_2010, Comp_2013)
# ----------------------------------------------------------------------------------------------------------------------------------------#
def concatCSVs():
    dtEscolaPublica2010 = escolasMunicipioPE2010()
    dtEscolaPublica2013 = escolasMunicipioPE2013()
    concatData = pd.DataFrame.merge(dtEscolaPublica2010, dtEscolaPublica2013,on=['municipio'],how='inner').reset_index()
    return concatData
# ----------------------------------------------------------------------------------------------------------------------------------------#
#Crita um dataframe com todos os municpios que têm menos e mais do que 100 computadores na soma total das escolas, nessa ordem.
# ----------------------------------------------------------------------------------------------------------------------------------------#
def cidMenos100Comp2010():
    escolasMunicipioPE = escolasMunicipioPE2010().reset_index()
    cidMenos100_2010 = escolasMunicipioPE.loc[(escolasMunicipioPE['Comp_2010'] < 100)]
    return cidMenos100_2010

def cidMais100Comp2010():
    escolasMunicipioPE = escolasMunicipioPE2010().reset_index()
    cidMais100_2010 = escolasMunicipioPE.loc[(escolasMunicipioPE['Comp_2010'] > 100)]
    return cidMais100_2010
# ----------------------------------------------------------------------------------------------------------------------------------------#

# ----------------------------------------------------------------------------------------------------------------------------------------#
def plotCidQuantCompAnos():
    concatData = concatCSVs()
    concatData = concatData[['Comp_2010','Comp_2013']]
    concatData.plot( kind="bar",stacked=True)
    plt.title('titulo') 
    plt.show()
# ----------------------------------------------------------------------------------------------------------------------------------------#

# ----------------------------------------------------------------------------------------------------------------------------------------#    
def plotMapa2010():
    dtEscolaPublica2010 = escolasMunicipioPE2010().reset_index()
    mapaDigitalDt = pd.DataFrame(mapaPE)
    dtEscolaPublica2010.drop_duplicates(inplace=True)
    dtEscolaPublica2010['CD_GEOCODM'] = dtEscolaPublica2010['municipio'].apply(int)
    mapaDigitalDt['CD_GEOCODM'] =  mapaDigitalDt['CD_GEOCODM'].apply(int)

    mapa = pd.merge(mapaDigitalDt, dtEscolaPublica2010, how='left', on='CD_GEOCODM')
    mapa = gpd.GeoDataFrame(mapa)
    mapa.plot(column='Comp_2010', cmap = 'RdYlGn_r', )
    plt.xlabel('Quantidade de computadores 2010')

def plotMapa2013():
    dtEscolaPublica2013 = escolasMunicipioPE2013().reset_index()
    mapaDigitalDt = pd.DataFrame(mapaPE)
    dtEscolaPublica2013.drop_duplicates(inplace=True)
    dtEscolaPublica2013['CD_GEOCODM'] = dtEscolaPublica2013['municipio'].apply(int)
    mapaDigitalDt['CD_GEOCODM'] =  mapaDigitalDt['CD_GEOCODM'].apply(int)
    
    mapa = pd.merge(mapaDigitalDt, dtEscolaPublica2013, how='left', on='CD_GEOCODM')
    mapa = gpd.GeoDataFrame(mapa)
    mapa.plot(column='Comp_2013', cmap = 'Accent')
    plt.xlabel('Quantidade de computadores 2013')
# ----------------------------------------------------------------------------------------------------------------------------------------#

# ----------------------------------------------------------------------------------------------------------------------------------------#
def plotCidVariacaoComp2010(): 
    cidMenos100 = cidMenos100Comp2010()
    cidMais100 = cidMais100Comp2010()
    mapaDigitalDt = pd.DataFrame(mapaPE)
    cidMenos100['CD_GEOCODM'] = cidMenos100['municipio'].apply(int)
    cidMais100['CD_GEOCODM'] = cidMais100['municipio'].apply(int)    
    mapaDigitalDt['CD_GEOCODM'] =  mapaDigitalDt['CD_GEOCODM'].apply(int)

  
    menos100 = pd.merge(mapaDigitalDt, cidMenos100, how='inner', on='CD_GEOCODM')
    mais100 = pd.merge(mapaDigitalDt, cidMais100, how='inner', on='CD_GEOCODM')    
    menos100 = gpd.GeoDataFrame(menos100)
    mais100 = gpd.GeoDataFrame(mais100)
               
    fig, ax = plt.subplots()
    mapaPE.plot(ax=ax, color='white', edgecolor='black')
    menos100.centroid.plot(ax=ax, color='red', markersize=20)  
    mais100.centroid.plot(ax=ax, color='blue', markersize=20)   
# ----------------------------------------------------------------------------------------------------------------------------------------#         
def main():
    
# --------- Metódos para imprimir as tabelas dos datasets, opicional só para a averiguação 
 
#     print(escolasMunicipioPE2010())
#     print(escolasMunicipioPE2013())
#     print(concatCSVs())
#     print(cidMenos100Comp2010())
#     print(cidMais100Comp2010())
    
# --------- Metódos para plotagem dos Gráficos
    
#     plotCidQuantCompAnos()
#     plotMapa2010()
#     plotMapa2013()
#     plotCidVariacaoComp2010()
     plt.show()


main()


#codigo de Recife == 2611606.0
