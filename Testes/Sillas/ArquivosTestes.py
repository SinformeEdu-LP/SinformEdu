import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd


datasetEscola2010 = pd.read_csv(r'C:\Users\silli\OneDrive\Documentos\GitHub\SinformEdu\Testes\python\arquivos\escolas2010.csv',low_memory=False, encoding='ISO-8859-1', sep='|')
datasetEscola2013 = pd.read_csv(r'C:\Users\silli\OneDrive\Documentos\GitHub\SinformEdu\Testes\python\arquivos\escolas2013.csv',low_memory=False, encoding='ISO-8859-1', sep='|')
mapaPE = gpd.read_file(r'C:\Users\silli\OneDrive\Documentos\GitHub\SinformEdu\Testes\python\arquivos\Shapes\PE\26MUE250GC_SIR.shp')


def escolasMunicipioPE2010():
    dtEscolaPublica2010 = datasetEscola2010.loc[(datasetEscola2010['ID_DEPENDENCIA_ADM'] < 4 ) & (datasetEscola2010['SIGLA'] == "PE" )]
    dtEscolaPublica2010 = dtEscolaPublica2010[['NUM_COMPUTADORES','FK_COD_MUNICIPIO']]
    dtEscolaPublica2010.columns = ['Comp_2010','municipio']
    
    return dtEscolaPublica2010

def escolasMunicipioPE2013():
    dtEscolaPublica2013 = datasetEscola2013.loc[(datasetEscola2013['ID_DEPENDENCIA_ADM'] == 3 ) & (datasetEscola2013['SIGLA'] == "PE" )]
    dtEscolaPublica2013 = dtEscolaPublica2013[['NUM_COMPUTADORES','FK_COD_MUNICIPIO']]
    dtEscolaPublica2013.columns = ['Comp_2013','municipio']
    return dtEscolaPublica2013

def cidMenos100Comp2010():
    cidMenos100Comp2010 = datasetEscola2010.loc[(datasetEscola2010['ID_DEPENDENCIA_ADM'] < 4 ) & (datasetEscola2010['SIGLA'] == "PE" )]
    cidMenos100Comp2010 = cidMenos100Comp2010[['NUM_COMPUTADORES','FK_COD_MUNICIPIO']]
    cidMenos100Comp2010.columns = ['Comp_2010','municipio']
    cidMenos100Comp2010 = cidMenos100Comp2010.groupby(['municipio']).Comp_2010.sum().to_frame().reset_index()
    cidMenos100Comp2010 = cidMenos100Comp2010.loc[(cidMenos100Comp2010['Comp_2010'] < 100)]
    return cidMenos100Comp2010

def cidMais100Comp2010():
    cidMais100Comp2010 = datasetEscola2010.loc[(datasetEscola2010['ID_DEPENDENCIA_ADM'] < 4 ) & (datasetEscola2010['SIGLA'] == "PE" )]
    cidMais100Comp2010 = cidMais100Comp2010[['NUM_COMPUTADORES','FK_COD_MUNICIPIO']]
    cidMais100Comp2010.columns = ['Comp_2010','municipio']
    cidMais100Comp2010 = cidMais100Comp2010.groupby(['municipio']).Comp_2010.sum().to_frame().reset_index()
    cidMais100Comp2010 = cidMais100Comp2010.loc[(cidMais100Comp2010['Comp_2010'] > 100)]
    return cidMais100Comp2010

def concatCSVs():
    dtEscolaPublica2010 = escolasMunicipioPE2010().groupby(['municipio']).Comp_2010.sum().to_frame()
    dtEscolaPublica2013 = escolasMunicipioPE2013().groupby(['municipio']).Comp_2013.sum().to_frame()
    concatData = pd.DataFrame.merge(dtEscolaPublica2010, dtEscolaPublica2013,on=['municipio'],how='inner').reset_index()
    return concatData

def plot():
    concatData = concatCSVs()
    concatData = concatData[['Comp_2010','Comp_2013']]
    concatData.plot( kind="line")
    plt.title('titulo') 
    plt.show()
    
def plotMapa2010():
    dtEscolaPublica2010 = escolasMunicipioPE2010()
    mapaDigitalDt = pd.DataFrame(mapaPE)
    dtEscolaPublica2010.drop_duplicates(inplace=True)
    dtEscolaPublica2010['CD_GEOCODM'] = dtEscolaPublica2010['municipio'].apply(int)
    mapaDigitalDt['CD_GEOCODM'] =  mapaDigitalDt['CD_GEOCODM'].apply(int)
    
    mapa = pd.merge(mapaDigitalDt, dtEscolaPublica2010, how='left', on='CD_GEOCODM')
    mapa = gpd.GeoDataFrame(mapa)
    mapa.plot(column='Comp_2010', cmap = 'RdYlGn_r', )

    plt.xlabel('Quantidade de computadores 2010')
    plt.savefig('Mapacomputadores2010.png')  
#     print('Figura "MapaInfraestruturaEscolasPorCidade.png" salva na pasta do projeto.')  

def plotMapa2013():
    dtEscolaPublica2013 = escolasMunicipioPE2013()
    mapaDigitalDt = pd.DataFrame(mapaPE)
    dtEscolaPublica2013.drop_duplicates(inplace=True)
    dtEscolaPublica2013['CD_GEOCODM'] = dtEscolaPublica2013['municipio'].apply(int)
    mapaDigitalDt['CD_GEOCODM'] =  mapaDigitalDt['CD_GEOCODM'].apply(int)
    
    mapa = pd.merge(mapaDigitalDt, dtEscolaPublica2013, how='left', on='CD_GEOCODM')
    mapa.to_csv('mapa_out.csv',';')
    mapa = gpd.GeoDataFrame(mapa)
    mapa.plot(column='Comp_2013', cmap = 'RdYlGn_r', )

    plt.xlabel('Quantidade de computadores 2013')
    plt.savefig('Mapacomputadores2013.png')

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
         
def main():

#     dtEscolaPublica2010 = escolasMunicipioPE2010()
#     print(cidMenos200)
#     print(dtEscolaPublica2010)
# #      plot()
#     plotMapa2010()     
#     plotMapa2013()
#     plotcidMenos200Comp2010()

# #     print(mapaPE.columns)
# #     cents2 = mapaPE.centroid
# #     cents= mapaPE[['geometry']]
# # 
# #     
    plotCidVariacaoComp2010()   
# #     fig, ax = plt.subplots()
# #     ax.set_aspect('equal')
# #     cents.plot(ax=ax, color='white', edgecolor='black')
# #     cents2.plot(ax=ax, color='red', markersize=5)
#     
    plt.show()
main()


#codigo de Recife == 2611606.0
