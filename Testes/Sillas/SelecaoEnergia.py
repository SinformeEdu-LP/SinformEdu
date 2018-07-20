import matplotlib.pyplot as plt
import pandas as pd

datasetEscola2010 = pd.read_csv(r'C:\Users\silli\OneDrive\Documentos\Pandas Testes\escolas2010.csv',low_memory=False, encoding='ISO-8859-1', sep='|')
datasetEscola2013 = pd.read_csv(r'C:\Users\silli\OneDrive\Documentos\Pandas Testes\escolas2013.csv',low_memory=False, encoding='ISO-8859-1', sep='|')

dtEscolaPublica2013 = datasetEscola2013.loc[(datasetEscola2013['ID_DEPENDENCIA_ADM'] < 4 ) & (datasetEscola2013['FK_COD_MUNICIPIO'] == 2611606 )
                                            & (datasetEscola2013['ID_ENERGIA_REDE_PUBLICA'] == 1)]
dtEscolaPublica2013 = dtEscolaPublica2013[['NO_ENTIDADE']]
print(dtEscolaPublica2013)

dtEscolaPublica2010 = datasetEscola2010.loc[(datasetEscola2010['ID_DEPENDENCIA_ADM'] < 4 ) & (datasetEscola2010['FK_COD_MUNICIPIO'] == 2611606.0 )
                                            & (datasetEscola2010['ID_ENERGIA_REDE_PUBLICA'] == 1)]
dtEscolaPublica2010 = dtEscolaPublica2010[['NO_ENTIDADE']]
print(dtEscolaPublica2010)
 
concat = pd.DataFrame.merge(dtEscolaPublica2010, dtEscolaPublica2013,
                         on=['NO_ENTIDADE'],
                         how='inner')
  
 

print(concat)
# concat.plot()
#  
# plt.show()
