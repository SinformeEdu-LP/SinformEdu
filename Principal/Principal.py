from Arquivos.Pontuacao_Escolas_Por_Municipio import gerarListaTabelasPontuacaoEscolas
from Arquivos.ValorInvestidoPorLocal import gerarListaEscolasConvenios
from Arquivos.PlotMapsCircleMarkers import plotMapCircleMarkers, plotarGraficosEscolasConvenios

def gerarGraficoMapa(local, listaAnos):
    listaPontuacaoEscolas = gerarListaTabelasPontuacaoEscolas(local, listaAnos)
    listaEscolasConvenio = gerarListaEscolasConvenios(local, listaPontuacaoEscolas, listaAnos)
    plotarGraficosEscolasConvenios(local, listaEscolasConvenio, listaAnos)
    
listaAnos = ['2015']#,'2015','2017']
local = 'BR' # Inserir a Sigla do Estado para mostrar as cidades ou 'BR' para mostrar os estados
    
gerarGraficoMapa(local, listaAnos)

