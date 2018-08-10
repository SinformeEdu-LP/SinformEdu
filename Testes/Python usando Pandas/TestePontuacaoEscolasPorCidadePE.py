import folium
import pandas as pd
from boto.sdb.db.sequence import double
from _cffi_backend import string

pd.set_option("display.max_columns",166)
from IPython import get_ipython
ipy = get_ipython()
if ipy is not None:
    ipy.run_line_magic('matplotlib', 'inline')
    ipy.run_line_magic('pylab', 'inline')
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import geopandas as gpd

df = pd.read_csv('mediaPontuacaoEscolasPorMunicipio2013_PE_out.csv',low_memory=False, sep=';')
df.rename(columns={'COD_MUNIC_IBGE':'CD_GEOCODM'}, inplace=True)
df['CD_GEOCODM'] = df['CD_GEOCODM'].apply(int).apply(str)
df['PONTUACAO_ESCOLAS_POR_CIDADE'] = df['PONTUACAO_ESCOLAS_POR_CIDADE'].apply(int)
df.to_csv('~/Documentos/Pandas Testes/dfff_out.csv',';')
df = df.fillna(0) #Converte NaN para 0
#df = df.loc[(df['PONTUACAO_ESCOLAS_POR_CIDADE'] < 300000)] # Sem Recife


def valorRepasse(valor):
    if valor == 0:
        result = ''
    else:
        #result = int(valor/10000) #mediana
        result = int(valor/1000000)+6
        #result = int(valor/100000)+6 # Sem Recife
    return result

def colorGraf(valor):
    if valor >= 25000:
        colorCirc = "#FF4A10" #Vermelho
    else:
        colorCirc = "#2917FF" #Azul
    return colorCirc

def plotCirculo(i):
    folium.CircleMarker([mapadigitalGeo.centroid.iloc[i].coords[0][1], mapadigitalGeo.centroid.iloc[i].coords[0][0] ],
                  radius = valorRepasse(mapadigital.iloc[i]['SOMA_VALOR_REPASSE_POR_CIDADE']),
                  popup=str(mapadigital.iloc[i]['NM_MUN_2017']),
                  color=colorGraf(mapadigital.iloc[i]['PONTUACAO_ESCOLAS_POR_CIDADE']),
                  fill=True,
                  line_opacity=0.1,
                  fill_opacity=0.4
                 ).add_to(mapFolium)
                 
# Location para mostrar o mapa de Pernambuco
mapFolium = folium.Map(location=[-8.31117289, -37.95566898], zoom_start=8) # Location -> Coordenadas do centro do Mapa a ser visualizado

mapadigital = gpd.read_file('/home/jrocha/Documentos/Pandas Testes/geo/26MUE250GC_SIR.shp')
mapadigitalGeo = gpd.GeoDataFrame(mapadigital)
gjson = mapadigital.to_crs(epsg='4326').to_json()

print(mapadigital)

mapadigital = pd.merge(mapadigitalGeo, df, how='inner', on='CD_GEOCODM')

mapFolium.choropleth(geo_data=gjson, data=mapadigital,
        columns=['CD_GEOCODM', 'PONTUACAO_ESCOLAS_POR_CIDADE','SOMA_VALOR_REPASSE_POR_CIDADE', 'NM_MUN_2017'],
        key_on='feature.properties.CD_GEOCODM',
        fill_color='YlGn',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='INFRAESTRUTURA DAS ESCOLAS (PONTOS)',
        reset=True)

sequencia = list(range(len(mapadigital)-1))
list(map(lambda x: plotCirculo(x), sequencia)) # Add ao mapa, os marcadores circulares
                 
mapFolium.save(outfile = 'PropostaXEscolas.html')
print('Gráfico salvo na pasta do arquivo .py !')



