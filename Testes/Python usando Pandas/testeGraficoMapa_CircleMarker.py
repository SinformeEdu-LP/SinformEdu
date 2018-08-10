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
    if valor >= 470:
        colorCirc = "#FF4A10" #Vermelho
    else:
        colorCirc = "#2917FF" #Azul
    return colorCirc

def plotCirculo(i):
    folium.CircleMarker([mapadigitalGeo.centroid.iloc[i].coords[0][1], mapadigitalGeo.centroid.iloc[i].coords[0][0] ],
                  radius=3,
                  popup=str(mapadigital.iloc[i]['ID']),
                  color=colorGraf(mapadigital.iloc[i]['ID']),
                  fill=True,
                  line_opacity=0.1,
                  fill_opacity=0.8
                 ).add_to(mapFolium)
                 
# Location para mostrar o mapa de Pernambuco
mapFolium = folium.Map(location=[-8.31117289, -37.95566898], zoom_start=8) # Location -> Coordenadas do centro do Mapa a ser visualizado

mapadigital = gpd.read_file('/home/jrocha/Documentos/Pandas Testes/geo/26MUE250GC_SIR.shp')
mapadigitalGeo = gpd.GeoDataFrame(mapadigital)
gjson = mapadigital.to_crs(epsg='4326').to_json()

mapFolium.choropleth(geo_data=gjson, data=mapadigital,
        columns=['CD_GEOCODM', 'ID'],
        key_on='feature.properties.CD_GEOCODM',
        fill_color='YlGn',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Taxa de ID (%)')

sequencia = list(range(len(mapadigital)-1))
list(map(lambda x: plotCirculo(x), sequencia)) # Add ao mapa, os marcadores circulares
                 
mapFolium.save(outfile = 'test6.html')
print('Gráfico salvo na pasta do arquivo .py !')



