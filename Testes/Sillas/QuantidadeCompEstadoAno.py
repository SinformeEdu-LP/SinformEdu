import matplotlib.pyplot as plt
import pandas as pd
#Selecionar os arquivos CSV e passar para um dataset
datasetEscola2010 = pd.read_csv(r'C:\Users\silli\OneDrive\Documentos\GitHub\SinformEdu\arquivos\escolas2010.csv',low_memory=False, encoding='ISO-8859-1', sep='|')
datasetEscola2011 = pd.read_csv(r'C:\Users\silli\OneDrive\Documentos\GitHub\SinformEdu\arquivos\escolas2011.csv',low_memory=False, encoding='ISO-8859-1', sep='|')
datasetEscola2012 = pd.read_csv(r'C:\Users\silli\OneDrive\Documentos\GitHub\SinformEdu\arquivos\escolas2012.csv',low_memory=False, encoding='ISO-8859-1', sep='|')
datasetEscola2013 = pd.read_csv(r'C:\Users\silli\OneDrive\Documentos\GitHub\SinformEdu\arquivos\escolas2013.csv',low_memory=False, encoding='ISO-8859-1', sep='|')

def escolasPorEstado2010():
    dtEscolaPublica2010 = datasetEscola2010.loc[(datasetEscola2010['ID_DEPENDENCIA_ADM'] < 4 )]
    dtEscolaPublica2010 = dtEscolaPublica2010[['NUM_COMPUTADORES','SIGLA']]
    dtEscolaPublica2010.columns = ['N_Comp_2010','SIGLA']
    qtdComp2010Estado = dtEscolaPublica2010.groupby(['SIGLA']).N_Comp_2010.sum().to_frame()
    return qtdComp2010Estado
def escolasPorEstado2011():     
    dtEscolaPublica2011 = datasetEscola2011.loc[(datasetEscola2011['ID_DEPENDENCIA_ADM'] < 4 )]
    dtEscolaPublica2011 = dtEscolaPublica2011[['NUM_COMPUTADORES','SIGLA']]
    dtEscolaPublica2011.columns = ['N_Comp_2011','SIGLA']
    qtdComp2011Estado = dtEscolaPublica2011.groupby(['SIGLA']).N_Comp_2011.sum().to_frame()
    return qtdComp2011Estado
def escolasPorEstado2012():
    dtEscolaPublica2012 = datasetEscola2012.loc[(datasetEscola2012['ID_DEPENDENCIA_ADM'] < 4 )]
    dtEscolaPublica2012 = dtEscolaPublica2012[['NUM_COMPUTADORES','SIGLA']]
    dtEscolaPublica2012.columns = ['N_Comp_2012','SIGLA']
    qtdComp2012Estado = dtEscolaPublica2012.groupby(['SIGLA']).N_Comp_2012.sum().to_frame()
    return qtdComp2012Estado
def escolasPorEstado2013():
    dtEscolaPublica2013 = datasetEscola2013.loc[(datasetEscola2013['ID_DEPENDENCIA_ADM'] < 4 )]
    dtEscolaPublica2013 = dtEscolaPublica2013[['NUM_COMPUTADORES', 'SIGLA']]
    dtEscolaPublica2013.columns = ['N_Comp_2013','SIGLA']
    qtdComp2013Estado = dtEscolaPublica2013.groupby(['SIGLA']).N_Comp_2013.sum().to_frame()
    return qtdComp2013Estado
def concatDataFrames():
    qtdComp2010Estado = escolasPorEstado2010()
    qtdComp2011Estado = escolasPorEstado2011()
    qtdComp2012Estado = escolasPorEstado2012()
    qtdComp2013Estado = escolasPorEstado2013()
    
    concat = pd.DataFrame.merge(qtdComp2010Estado, qtdComp2011Estado,
                             on=['SIGLA'],
                             how='inner')
    concat2 = pd.DataFrame.merge(qtdComp2012Estado,qtdComp2013Estado,
                             on=['SIGLA'],
                             how='inner')
    concat3 = pd.DataFrame.merge(concat,concat2,
                             on=['SIGLA'],
                             how='inner')
    return concat3
def plotBarrasAninhadas():
    concat3 = concatDataFrames()
    concat3.plot(kind = "bar",stacked=True)
    plt.title('Quantidade de Computadores por Ano/Estado')
    plt.xlabel('Estados')
    plt.legend(["2010","2011","2012","2013"])
    plt.ylabel('Quantidade de Computadores')
    plt.show()

def main():
    plotBarrasAninhadas()
main()

