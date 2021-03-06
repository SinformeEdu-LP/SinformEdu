from Arquivos.PontuacaoEscolasPorMunicipio import gerarListaTabelasPontuacaoEscolas
from Arquivos.ValorInvestidoPorLocal import gerarListaEscolasConvenios
from Arquivos.PlotMapsCircleMarkers import plotarGraficosEscolasConvenios
from Arquivos.EmendasPorPartido import gerarGraficosEmendaPorPartido
from Arquivos.IOEBxItensEscolasPorCidade import gerarGraficosCorrelacesItensXIOEB

def gerarGraficoMapa(local, listaAnos):
    listaPontuacaoEscolas = gerarListaTabelasPontuacaoEscolas(local, listaAnos)
    listaEscolasConvenio = gerarListaEscolasConvenios(local, listaPontuacaoEscolas, listaAnos)
    plotarGraficosEscolasConvenios(local, listaEscolasConvenio, listaAnos)
    
listaAnos = ['2013','2015','2017']
#local = 'BR' # Inserir a Sigla do Estado para mostrar as cidades ou 'BR' para mostrar os estados

gerarGraficosEmendaPorPartido()
gerarGraficosCorrelacesItensXIOEB()
    
gerarGraficoMapa('BR', listaAnos)
gerarGraficoMapa('PE', listaAnos)
#gerarGraficoMapa('CE', listaAnos)
#gerarGraficoMapa('PB', listaAnos)
#gerarGraficoMapa('SP', listaAnos)
#gerarGraficoMapa('RN', listaAnos)
print('Fim da Execução do Programa.')