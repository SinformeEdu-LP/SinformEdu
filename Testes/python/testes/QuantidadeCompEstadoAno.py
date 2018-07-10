import matplotlib.pyplot as plt
import pandas as pd
#Selecionar os arquivos CSV e passar para um dataset
datasetEscola2010 = pd.read_csv(r'C:\Users\silli\OneDrive\Documentos\GitHub\SinformEdu\Testes\python\arquivos\escolas2010.csv',low_memory=False, encoding='ISO-8859-1', sep='|')
datasetEscola2013 = pd.read_csv(r'C:\Users\silli\OneDrive\Documentos\GitHub\SinformEdu\Testes\python\arquivos\escolas2013.csv',low_memory=False, encoding='ISO-8859-1', sep='|')

#Selecionar as Colunas Desejadas do dataset e Renomear para ficar fácil sua identificação
dtEscolaPublica2010 = datasetEscola2010.loc[(datasetEscola2010['ID_DEPENDENCIA_ADM'] < 4 )]
dtEscolaPublica2010 = dtEscolaPublica2010[['NUM_COMPUTADORES','SIGLA']]
dtEscolaPublica2010.columns = ['N_Comp_2010','SIGLA']

dtEscolaPublica2013 = datasetEscola2013.loc[(datasetEscola2013['ID_DEPENDENCIA_ADM'] < 4 )]
dtEscolaPublica2013 = dtEscolaPublica2013[['NUM_COMPUTADORES', 'SIGLA']]
dtEscolaPublica2013.columns = ['N_Comp_2013','SIGLA']

qtdComp2010Estado = dtEscolaPublica2010.groupby(['SIGLA']).N_Comp_2010.sum().to_frame()
qtdComp2013Estado = dtEscolaPublica2013.groupby(['SIGLA']).N_Comp_2013.sum().to_frame()

concat = pd.DataFrame.merge(qtdComp2010Estado, qtdComp2013Estado,
                         on=['SIGLA'],
                         how='inner')


concat.plot(x = 'SIGLA', kind = "bar")
plt.title('Quantidade de Computadores por Ano/Estado')
plt.xlabel('Estados')
plt.ylabel('Quantidade de Computadores')
plt.show()


