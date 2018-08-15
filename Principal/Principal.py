from Arquivos.Pontuacao_Escolas_Por_Municipio import gerarListaTabelasPontuacaoEscolas
from Arquivos.ValorInvestidoPorLocal import gerarListaEscolasConvenios
from Arquivos.PlotMapsCircleMarkers import plotMapCircleMarkers

listaAnos = ['2015']
local = 'BR' # Sigla do Estado para mostrar suas cidades ou BR para mostrar os estados

def gerarGraficoMapa(local, listaAnos):
    listaPontuacaoEscolas = gerarListaTabelasPontuacaoEscolas(local, listaAnos)
    listaEscolasConvenio = gerarListaEscolasConvenios(local, listaPontuacaoEscolas, listaAnos[0])
    plotMapCircleMarkers(listaEscolasConvenio[0], local, listaAnos[0])
    
gerarGraficoMapa(local, listaAnos)

