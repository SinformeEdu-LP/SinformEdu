import matplotlib.pyplot as plt
import pandas as pd

datasetEscola2010 = pd.read_csv(r'C:\Users\silli\OneDrive\Documentos\GitHub\SinformEdu\Testes\python\arquivos\escolas2010.csv',low_memory=False, encoding='ISO-8859-1', sep='|')
datasetEscola2013 = pd.read_csv(r'C:\Users\silli\OneDrive\Documentos\GitHub\SinformEdu\Testes\python\arquivos\escolas2013.csv',low_memory=False, encoding='ISO-8859-1', sep='|')


dtEscolaPublica2010 = datasetEscola2010.loc[(datasetEscola2010['ID_DEPENDENCIA_ADM'] < 4 ) & (datasetEscola2010['SIGLA'] == "PE" )]
dtEscolaPublica2010 = dtEscolaPublica2010[['NO_ENTIDADE','NUM_COMPUTADORES','FK_COD_MUNICIPIO']]
dtEscolaPublica2010.columns = ['Nome', 'Comp_2010','municipio']


dtEscolaPublica2013 = datasetEscola2013.loc[(datasetEscola2013['ID_DEPENDENCIA_ADM'] < 4 ) & (datasetEscola2013['SIGLA'] == "PE" )]
dtEscolaPublica2013 = dtEscolaPublica2013[['NO_ENTIDADE','NUM_COMPUTADORES','FK_COD_MUNICIPIO']]
dtEscolaPublica2013.columns = ['Nome', 'Comp_2013', 'municipio']

qtdComp2010Muni = dtEscolaPublica2010.groupby(['municipio']).Comp_2010.sum().to_frame()
qtdComp2013Muni = dtEscolaPublica2013.groupby(['municipio']).Comp_2013.sum().to_frame()

print(qtdComp2010Muni)
print(qtdComp2013Muni)

concat = pd.DataFrame.merge(qtdComp2010Muni, qtdComp2013Muni,
                         on=['municipio'],
                         how='inner').reset_index()

concat = concat[['Comp_2010','Comp_2013']]

mydata = [{'2010': concat['Comp_2010'].sum(), '2013': concat['Comp_2013'].sum()}]

df = pd.DataFrame(mydata)

print(df)

df.plot(kind="bar")
# plt.title('titulo') 
# 
plt.show()  
# BF_Valor = concat.groupby(['municipio']).Comp_2010.sum()
# print (BF_Valor)

#                                             & (datasetEscola2013['FK_COD_MUNICIPIO'] == 2611606.0 )]
