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

codEstados = pd.read_csv('./Dados/cod_estados.csv',low_memory=False, sep=';')

def colorGraf(valor):
    if valor >= 470:
        colorCirc = "#FF4A10" #Vermelho
    else:
        colorCirc = "#2917FF" #Azul
    return colorCirc

def plotCirculo(i):
    folium.CircleMarker([mapadigitalGeo.centroid.iloc[i].coords[0][1], mapadigitalGeo.centroid.iloc[i].coords[0][0] ],
                  radius=int( mapadigital.iloc[i]['ID']*10/184 + (3-4020/184) ),
                  popup=str(mapadigital.iloc[i]['ID']),
                  color=colorGraf(mapadigital.iloc[i]['ID']),
                  fill=True,
                  line_opacity=0.1,
                  fill_opacity=0.8
                 ).add_to(mapFolium)
                 
def dadosEstados(sigla):
    
    codEstados = pd.read_csv('./Dados/cod_estados.csv',low_memory=False, sep=';')
    codValor = codEstados.loc[result['SIGLA'] == sigla, 'COD'].values[0]
    latEstado = codEstados.loc[result['SIGLA'] == sigla, 'LAT'].values[0]
    longEstado = codEstados.loc[result['SIGLA'] == sigla, 'LONG'].values[0]
    coords = [latEstado,longEstado]
    
    ESTADO = {
        'nome_arquivo_shp': './Dados/Shapes/'+sigla+'/'+codValor+'MUE250GC_SIR.shp',
        'location': coords, # [Latitude, Longitude]
        'zoom': 8
    }
    return ESTADO

def plotMapCircleMarkers(dataframe, sigla):
    
    ESTADO = dadosEstados(sigla)
    mapFolium = folium.Map(location=ESTADO['location'], zoom_start=ESTADO['zoom'])
    mapadigital = gpd.read_file(ESTADO['nome_arquivo_shp'])
    mapadigitalGeo = gpd.GeoDataFrame(mapadigital)
    gjson = mapadigital.to_crs(epsg='4326').to_json()
    
    mapEstado.choropleth(geo_data=gjson, data=mapadigital,
            columns=['CD_GEOCODM', 'ID'],
            key_on='feature.properties.CD_GEOCODM',
            fill_color='YlGn',
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='Taxa de ID (%)')
    
    sequencia = list(range(len(mapadigital)-1))
    list(map(lambda x: plotCirculo(x), sequencia)) # Add ao mapa, os marcadores circulares
                     
    mapEstado.save(outfile = '~/Documentos/Pandas Testes/mapEstado_test6.html')
    print('Gráfico salvo na pasta do arquivo .py !')



