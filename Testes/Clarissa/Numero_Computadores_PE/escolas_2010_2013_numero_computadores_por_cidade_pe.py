import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Ler o csv
esc_2013 = pd.read_csv('/home/tonton/Downloads/2013/DADOS/ESCOLAS.CSV', sep='|', encoding = "ISO-8859-1", dtype = { 'FK_COD_MUNICIPIO': np.int64 })
municipios = pd.read_csv('/home/tonton/Downloads/municipios.csv', encoding = "UTF-8", dtype = { 'FK_COD_MUNICIPIO': np.int64 })
#Filtrar por alguma coluna especifica
esc_2013_funcionamento = esc_2013.loc[esc_2013['DESC_SITUACAO_FUNCIONAMENTO'] == 1]
esc_2013_funcionamento_estadual_municipal = esc_2013_funcionamento.loc[esc_2013_funcionamento['ID_DEPENDENCIA_ADM'].isin([1,2])]
esc_2013_pe = esc_2013_funcionamento_estadual_municipal.loc[esc_2013['SIGLA'] == "PE"]
#Um groupBy para agroupar as informações especificadas
comput_por_municipio_2013 = esc_2013_pe.filter(items=['NUM_COMPUTADORES', 'FK_COD_MUNICIPIO']).groupby(['FK_COD_MUNICIPIO']).sum()


municipios = municipios.set_index('FK_COD_MUNICIPIO')
join_final_2013 = comput_por_municipio_2013.join(municipios, on='FK_COD_MUNICIPIO').sort_values(by=['NUM_COMPUTADORES'], ascending=False)
#Filtro com as 10 cidades de maior pib
cidades_por_pib_2013 = join_final_2013.loc[join_final_2013['NOME_MUNICIPIO'].isin(['RECIFE','JABOATAO DOS GUARARAPES', 'IPOJUCA', 'CABO DE SANTO AGOSTINHO', 'CARUARU', 'PETROLINA', 'OLINDA', 'PAULISTA', 'GOIANA', 'VITORIA DE SANTO ANTAO'])]


#2010
esc_2010 = pd.read_csv('/home/tonton/Downloads/2010/DADOS/ESCOLAS.CSV', sep='|', encoding = "ISO-8859-1", dtype = { 'FK_COD_MUNICIPIO': np.int64 })
#Filtrar por alguma coluna especifica
esc_2010_funcionamento = esc_2010.loc[esc_2010['DESC_SITUACAO_FUNCIONAMENTO'] == 1]
esc_2010_funcionamento_estadual_municipal = esc_2010_funcionamento.loc[esc_2010_funcionamento['ID_DEPENDENCIA_ADM'].isin([1,2])]
esc_2010_pe = esc_2010_funcionamento_estadual_municipal.loc[esc_2010['SIGLA'] == "PE"]
#Um groupBy para agroupar as informações especificadas
comput_por_municipio_2010 = esc_2010_pe.filter(items=['NUM_COMPUTADORES', 'FK_COD_MUNICIPIO']).groupby(['FK_COD_MUNICIPIO']).sum()


municipios = municipios.set_index('FK_COD_MUNICIPIO')
join_final_2010 = comput_por_municipio_2010.join(municipios, on='FK_COD_MUNICIPIO').sort_values(by=['NUM_COMPUTADORES'], ascending=False)
#filtro com as 10 cidades por pib
cidades_por_pib_2010 = join_final_2010.loc[join_final_2010['NOME_MUNICIPIO'].isin(['RECIFE','JABOATAO DOS GUARARAPES', 'IPOJUCA', 'CABO DE SANTO AGOSTINHO', 'CARUARU', 'PETROLINA', 'OLINDA', 'PAULISTA', 'GOIANA', 'VITORIA DE SANTO ANTAO'])]

join_final_cidades_pe_2013_2010 = pd.merge(cidades_por_pib_2013, cidades_por_pib_2010, on=['FK_COD_MUNICIPIO','NOME_MUNICIPIO'])

#grafico
