import folium
import pandas as pd

maximoColunasMostradas = 170 
pd.set_option("display.max_columns",maximoColunasMostradas)
from IPython import get_ipython
ipy = get_ipython()
if ipy is not None:
    ipy.run_line_magic('matplotlib', 'inline')
    ipy.run_line_magic('pylab', 'inline')
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import geopandas as gpd
import locale
locale.setlocale(locale.LC_ALL, '') 

def colorGraf(valor, multiplicador):
    referenciaMinimaValor = 500000 # Abaixo desse valor (500 mil) foi convencionado ser o mínimo
    #Para a referencia máxima o valor foi ajustado de acordo com alguns resultados,
    #onde para os graficos de mapa de cada estado o multiplicador é 1, e para o Brasil é 10.
    referenciaMaximaValor = 1000000 * multiplicador
    if valor == 0:
        colorCirc = ''
    elif valor >= referenciaMaximaValor :
        colorCirc = "#13FF00" #Verde
    elif valor < referenciaMinimaValor:
        colorCirc = "#FF503B" #Vermelho
    else:
        colorCirc = "#E8D319" #Amarelo 
    return colorCirc

def valorTotal(valor, multiplicador):
    if valor != 0:
        referenciaMaximaValor = 10000000 * multiplicador
        referenciaMinimaCirculo = 2
        referenciaMaximaCirculo = 20
        #O valor que no caso passa de 100 milhoes no mapa BR foi escalonado para a faixa de 2 a 30 para ser plotado em bolhas
        result = referenciaMinimaCirculo+(referenciaMaximaCirculo-referenciaMinimaCirculo)*(valor)/(referenciaMaximaValor)
    else:
        result = '' #com valor nulo a bolha não aparece no mapa
    return result

def formatarPopup(valor):
    formatValor = 'R$ '+locale.format('%.2f', (valor), True)
    result = "<b> Valor Global: </b><br/>" +  str(formatValor)
    return result


def plotCirculo(i, mapadigitalGeo, mapadigital, mapFolium, multiplicador):
    folium.CircleMarker([mapadigitalGeo.centroid.iloc[i].coords[0][1], mapadigitalGeo.centroid.iloc[i].coords[0][0] ],
                  radius= valorTotal( mapadigital.iloc[i]['TOTAL_VL_GLOBAL_PROP'], multiplicador ),#mapadigital.iloc[i]['TOTAL_VL_GLOBAL_PROP']/10000,
                  popup=formatarPopup( mapadigital.iloc[i]['TOTAL_VL_GLOBAL_PROP'] ), #"<b>" + parada + "</b><br/>" + "media: " + str(dado)
                  color=colorGraf(mapadigital.iloc[i]['TOTAL_VL_GLOBAL_PROP'], multiplicador),
                  fill=True,
                  line_opacity=0.1,
                  fill_opacity=0.4
                 ).add_to(mapFolium)
                 
def dadosLocal(local):
    if local == 'BR':
        latBrasil = -14.235004 #latitude central aproximada do Brasil
        longBrasil = -51.92528 #latitude central aproximada do Brasil
        coords = [latBrasil, longBrasil]
        zoomInicialMapa = 5
        RESULT = {
            'arquivoShape': './Dados/Shapefiles/'+local+'-UF/BRUFE250GC_SIR.shp',
            'localMap': coords, # [Latitude, Longitude]
            'zoomMap': zoomInicialMapa,
            'chaveMap': 'CD_GEOCUF',
            'multiplicador': 50
        }
    else:
        codEstados = pd.read_csv('./Dados/cod_estados.csv',low_memory=False, sep=';')
        codValor = codEstados.loc[codEstados['SIGLA'] == local, 'COD'].values[0]
        latEstado = codEstados.loc[codEstados['SIGLA'] == local, 'LAT'].values[0]
        longEstado = codEstados.loc[codEstados['SIGLA'] == local, 'LONG'].values[0]
        coords = [latEstado,longEstado]
        zoomInicialMapa = 7
        RESULT = {
            'arquivoShape': './Dados/Shapefiles/'+local+'-MUN/'+str(codValor)+'MUE250GC_SIR.shp',
            'localMap': coords, # [Latitude, Longitude]
            'zoomMap': zoomInicialMapa,
            'chaveMap': 'CD_GEOCODM',
            'multiplicador': 1
        }
    return RESULT

def converterTipoColunas(df, chaveMap):
    df[chaveMap] = df[chaveMap].apply(int).apply(str)
    df['TOTAL_VL_GLOBAL_PROP'] = df['TOTAL_VL_GLOBAL_PROP'].astype(float)#apply(float)
    df['MEDIA_PONTUACAO_ESCOLAS_POR_CIDADE'] = df['MEDIA_PONTUACAO_ESCOLAS_POR_CIDADE'].apply(int)
    df = df.fillna(0) #Converte NaN para 0
    return df

def formatarPopupMapa(tipoLocal):
    result = "MEDIA PONTUACAO ESCOLAS POR" + tipoLocal+"- Valor Total dos Convênios (Bolhas)"
    return result

def plotMapCircleMarkers(local, dataframe, ano):   
    RESULT = dadosLocal(local)
    dataframeTratado = converterTipoColunas(dataframe, RESULT['chaveMap'])
    
    mapadigital = gpd.read_file(RESULT['arquivoShape'])
    mapadigitalGeo = gpd.GeoDataFrame(mapadigital)
    gjson = mapadigital.to_crs(epsg='4326').to_json()
    
    mapadigital = pd.merge(mapadigitalGeo, dataframeTratado, how='left', on=RESULT['chaveMap']) # GEOCODM
    mapadigital = mapadigital.fillna(0) #Converte NaN para 0
    
    mapFolium = folium.Map(location=RESULT['localMap'], zoom_start=RESULT['zoomMap'])
    mapFolium.choropleth(geo_data=gjson, data=mapadigital,
            columns=[RESULT['chaveMap'], 'MEDIA_PONTUACAO_ESCOLAS_POR_CIDADE','TOTAL_VL_GLOBAL_PROP'],
            key_on='feature.properties.'+RESULT['chaveMap'],
            fill_color='YlGn',
            fill_opacity = 0.7,
            line_opacity = 0.2,
            popup = 'Teste1',
            legend_name = formatarPopupMapa('ESTADO')
            )
    
    sequencia = list(range(len(mapadigital)-1))
    list(map(lambda x: plotCirculo(x, mapadigitalGeo, mapadigital, mapFolium, RESULT['multiplicador']), sequencia)) # Add ao mapa, os marcadores circulares
                     
    mapFolium.save(outfile = './Resultados/Graficos/MapaInfraestrutura_X_BolhaConvenios'+ano+'_'+local+'.html')
    print('Gráfico_'+ano+'_'+local+' salvo na pasta Principal/Resultados/Graficos!')
    
def plotarGraficosEscolasConvenios(local, listaTabelaEscolas, listaAnos):
    listaEscolasConvenios = list(map(lambda x,y: plotMapCircleMarkers(local, x, y), listaTabelaEscolas, listaAnos))
    print('Todos os gráficos salvos!!')
    print('Etapa finalizada!')
    print()
    return listaEscolasConvenios



