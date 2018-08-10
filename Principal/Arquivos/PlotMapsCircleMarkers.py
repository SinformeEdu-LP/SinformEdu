import folium
import pandas as pd

pd.set_option("display.max_columns",166)
from IPython import get_ipython
ipy = get_ipython()
if ipy is not None:
    ipy.run_line_magic('matplotlib', 'inline')
    ipy.run_line_magic('pylab', 'inline')
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import geopandas as gpd

def colorGraf(valor):
    if valor == 0:
        colorCirc = ''
    elif valor >= 500000:
        colorCirc = "#13FF00" #Verde "#2917FF" #Azul
    elif valor < 150000:
        colorCirc = "#FF503B" #Vermelho
    else:
        colorCirc = "#E8D319" #Amarelo 
    return colorCirc

def valorTotal(valor):
    if valor == 0:
        result = ''
    elif valor >= 100000000:
        result = 2*valor/10000000
    elif valor >= 10000000:
        result = valor/1000000
    elif valor >= 1000000:
        result = valor/200000
    elif valor >= 100000:
        result = valor/40000
    elif valor >= 10000:
        result = valor/5000
    else:
        result = 1 
    return result


def plotCirculo(i, mapadigitalGeo, mapadigital, mapFolium):
    folium.CircleMarker([mapadigitalGeo.centroid.iloc[i].coords[0][1], mapadigitalGeo.centroid.iloc[i].coords[0][0] ],
                  radius= valorTotal( mapadigital.iloc[i]['TOTAL_VL_GLOBAL_PROP'] ),#mapadigital.iloc[i]['TOTAL_VL_GLOBAL_PROP']/10000,
                  popup=str(mapadigital.iloc[i]['TOTAL_VL_GLOBAL_PROP']),
                  color=colorGraf(mapadigital.iloc[i]['TOTAL_VL_GLOBAL_PROP']),
                  fill=True,
                  line_opacity=0.1,
                  fill_opacity=0.4
                 ).add_to(mapFolium)
                 
def dadosEstados(local):
    if local == 'BR':
        coords = [-9.588903,-51.619789]
        RESULT = {
            'nome_arquivo_shp': './Dados/Shapefiles/'+local+'-UF/BRUFE250GC_SIR.shp',
            'location': coords, # [Latitude, Longitude]
            'zoom': 5
        }
    else:
        codEstados = pd.read_csv('./Dados/cod_estados.csv',low_memory=False, sep=';')
        codValor = codEstados.loc[codEstados['SIGLA'] == local, 'COD'].values[0]
        latEstado = codEstados.loc[codEstados['SIGLA'] == local, 'LAT'].values[0]
        longEstado = codEstados.loc[codEstados['SIGLA'] == local, 'LONG'].values[0]
        coords = [latEstado,longEstado]
        RESULT = {
            'nome_arquivo_shp': './Dados/Shapefiles/'+local+'-MUN/'+str(codValor)+'MUE250GC_SIR.shp',
            'location': coords, # [Latitude, Longitude]
            'zoom': 8
        }
    return RESULT

def ajustarDataframe(df):
    df.rename(columns={'COD_MUNIC_IBGE':'CD_GEOCODM'}, inplace=True)
    df['CD_GEOCODM'] = df['CD_GEOCODM'].apply(int).apply(str)
    df['TOTAL_VL_GLOBAL_PROP'] = df['TOTAL_VL_GLOBAL_PROP'].apply(int)
    df['MEDIA_PONTUACAO_ESCOLAS_POR_CIDADE'] = df['MEDIA_PONTUACAO_ESCOLAS_POR_CIDADE'].apply(int)
    df.to_csv('~/Documentos/Pandas Testes/dfffrrrrrrr_out.csv',';')
    df = df.fillna(0) #Converte NaN para 0
    return df

def plotMapCircleMarkers(dataframe, local, ano):
    df = ajustarDataframe(dataframe)
    
    RESULT = dadosEstados(local)
    
    mapadigital = gpd.read_file(RESULT['nome_arquivo_shp'])
    mapadigitalGeo = gpd.GeoDataFrame(mapadigital)
    gjson = mapadigital.to_crs(epsg='4326').to_json()
    
    mapadigital = pd.merge(mapadigitalGeo, df, how='left', on='CD_GEOCODM')
    mapadigital = mapadigital.fillna(0) #Converte NaN para 0
    
    mapFolium = folium.Map(location=RESULT['location'], zoom_start=RESULT['zoom'])
    mapFolium.choropleth(geo_data=gjson, data=mapadigital,
            columns=['CD_GEOCODM', 'MEDIA_PONTUACAO_ESCOLAS_POR_CIDADE','TOTAL_VL_GLOBAL_PROP','NM_MUN_2017'],
            key_on='feature.properties.CD_GEOCODM',
            fill_color='YlGn',
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='INFRAESTRUTURA DAS ESCOLAS (PONTOS)')
    '''mapFolium.choropleth(geo_data=gjson, data=mapadigital,
            columns=['CD_GEOCUF', 'Score'],
            key_on='feature.properties.CD_GEOCUF',
            fill_color='YlGn',
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='Taxa de ID (%)')'''
    
    sequencia = list(range(len(mapadigital)-1))
    list(map(lambda x: plotCirculo(x, mapadigitalGeo, mapadigital, mapFolium), sequencia)) # Add ao mapa, os marcadores circulares
                     
    mapFolium.save(outfile = './Resultados/Graficos/mapEstado'+ano+'_'+local+'.html')
    print('Gráfico salvo na pasta Principal/Graficos!')



