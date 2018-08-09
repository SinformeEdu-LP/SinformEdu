import pandas as pd

pd.set_option("display.max_columns",166)
from IPython import get_ipython
ipy = get_ipython()
if ipy is not None:
    ipy.run_line_magic('matplotlib', 'inline')
    ipy.run_line_magic('pylab', 'inline')
import matplotlib.pyplot as plt
plt.style.use('ggplot')

TabelaInfra = ["NU_ANO_CENSO","CO_UF","CO_MUNICIPIO","IN_SALA_PROFESSOR","IN_LABORATORIO_INFORMATICA",
                "IN_LABORATORIO_CIENCIAS","IN_QUADRA_ESPORTES_COBERTA","IN_QUADRA_ESPORTES_DESCOBERTA","IN_COZINHA","IN_BIBLIOTECA",
                "IN_AUDITORIO","IN_PATIO_COBERTO","IN_PATIO_DESCOBERTO","NU_SALAS_EXISTENTES","NU_EQUIP_TV","NU_EQUIP_COPIADORA",
                "NU_EQUIP_IMPRESSORA","NU_EQUIP_SOM","NU_EQUIP_MULTIMIDIA","NU_COMP_ADMINISTRATIVO",
                "NU_COMP_ALUNO","IN_INTERNET","NU_FUNCIONARIOS","IN_ALIMENTACAO"]
ItensInfra = TabelaInfra[3:]
pesos = [20,50,40,50,25,20,40,25,30,15,5,3,10,5,10,4,5,3,20,10,40]
sequencia = list(range(len(ItensInfra)-1))

def agrupamentoTurmas(x):
    result = {
        'QTD_ALUNOS_POR_ESCOLA': x['NU_MATRICULAS'].sum()
    }
    return pd.Series(result)

def agrupamentoMunicipio(x):
    result = {'NU_ANO_CENSO': x['NU_ANO_CENSO'].min(),
              'CO_ENTIDADE': x['CO_ENTIDADE'].min(),
              'MEDIA_QTD_ALUNOS_POR_ESCOLA': x['QTD_ALUNOS_POR_ESCOLA'].mean(),
              'MEDIA_NU_COMP_PARA_ALUNOS': x['NU_COMP_ALUNO'].mean(),
              'COMP_POR_ALUNO(%)': x['NUM_COMP_POR_ALUNO'].mean(),
              'NUM_ESCOLAS_INTERNET_MUNIC': x['IN_INTERNET'].sum(),
              'MEDIA_SALAS_EXISTENTES': x['NU_SALAS_EXISTENTES'].mean(),
              'MEDIA_PONTUACAO': x['PONTUACAO'].mean()
    }
    return pd.Series(result)

def gerarTabelaItensEscolas(ano): # Gera uma tabela para correlacionar com algum índice
    dfEscolas = pd.read_csv('../arquivos/escolas'+ano+'.csv',low_memory=False, encoding='ISO-8859-1', sep='|')
    dfEscolas["PONTUACAO"] = sum( list(map(lambda x,y: x * dfEscolas[ItensInfra[y]], pesos, sequencia)) )
    dfEscolas = dfEscolas[['NU_ANO_CENSO', 'CO_ENTIDADE', 'CO_MUNICIPIO' ,'NU_COMP_ALUNO', 'IN_INTERNET', 'NU_SALAS_EXISTENTES', 'PONTUACAO']] 
    dfEscolas.to_csv('itensPorEscolas'+ano+'_out.csv','|')
    return dfEscolas

def gerarTabelaQtdAlunosPorEscola(ano): # Gera uma tabela com a qtd de alunos por escola
    dfTurmas = pd.read_csv('../arquivos/turmas'+ano+'.csv',low_memory=False, encoding='ISO-8859-1', sep='|')
    dfTurmasAgrupado = dfTurmas.groupby('CO_ENTIDADE')
    tabelaQtdAlunosPorEscola = dfTurmasAgrupado.apply(agrupamentoTurmas)
    tabelaQtdAlunosPorEscola.to_csv('qtdAlunosPorEscola'+ano+'_out.csv','|')
    return tabelaQtdAlunosPorEscola

def mergeTabelas(ano): # Faz o merge de ItensEscolas com QtdAlunosPorEscola
    itensEscolas = pd.read_csv('../arquivos/correlacao/itensPorEscolas'+ano+'_out.csv',low_memory=False, encoding='ISO-8859-1', sep='|')
    qtdAlunosEscola = pd.read_csv('../arquivos/correlacao/qtdAlunosPorEscola'+ano+'_out.csv',low_memory=False, encoding='ISO-8859-1', sep='|')
    mergeItens_QtdAlunos = pd.merge(itensEscolas, qtdAlunosEscola, how='inner', on='CO_ENTIDADE')
    mergeItens_QtdAlunos["NUM_COMP_POR_ALUNO"] = 100 * mergeItens_QtdAlunos['NU_COMP_ALUNO']/mergeItens_QtdAlunos['QTD_ALUNOS_POR_ESCOLA'] #% de Comp por Aluno
    mergeItens_QtdAlunos.to_csv('itens_Por_Escola'+ano+'_out.csv','|')
    tabelaItens_Municipio = agruparMunicipio(ano,mergeItens_QtdAlunos)
    return mergeItens_QtdAlunos, tabelaItens_Municipio

def agruparMunicipio(ano,tabela):  #Tabela para correlacionar com IOEB 
    tabelaAgrupada = tabela.groupby('CO_MUNICIPIO')
    tabelaItens_Municipio = tabelaAgrupada.apply(agrupamentoMunicipio)
    tabelaItens_Municipio.to_csv('itens_Por_Municipio'+ano+'_out.csv','|')
    return tabelaItens_Municipio

lista_anos = ['2015','2017']

#listaTabelasQtdAlunosPorEscola = list(map(lambda x: gerarTabelaQtdAlunosPorEscola(x), lista_anos)) #Roda só um vez, gerando as tabelas

#listaTabelasItensEscolas = list(map(lambda x: gerarTabelaItensEscolas(x), lista_anos)) #Roda só um vez, gerando as tabelas

listaItensPorEscola, listaItensPorMunicipio = list(map(lambda x: mergeTabelas(x), lista_anos)) #Roda só um vez, gerando as tabelas











