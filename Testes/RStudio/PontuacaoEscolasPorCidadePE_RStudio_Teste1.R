library(leaflet)
library(tidyverse)
library(stringr)
library(dplyr)
library(readr)
library(readxl)
library(rgdal)

escolas2013 <- read_delim("/home/jrocha/Documentos/rStudio/geo/escolas2013.csv", delim = "|")

ItensInfra <- c("ANO_CENSO","SIGLA","FK_COD_MUNICIPIO","ID_DEPENDENCIA_ADM","ID_SALA_PROFESSOR","ID_LABORATORIO_INFORMATICA",
                "ID_LABORATORIO_CIENCIAS","ID_QUADRA_ESPORTES_COBERTA","ID_QUADRA_ESPORTES_DESCOBERTA","ID_COZINHA","ID_BIBLIOTECA",
                "ID_AUDITORIO","ID_PATIO_COBERTO","ID_PATIO_DESCOBERTO","NUM_SALAS_EXISTENTES","NUM_EQUIP_TV","NUM_EQUIP_COPIADORA",
                "NUM_EQUIP_IMPRESSORA","NUM_EQUIP_SOM","NUM_EQUIP_MULTIMIDIA","NUM_COMPUTADORES","NUM_COMP_ADMINISTRATIVOS",
                "NUM_COMP_ALUNOS","ID_INTERNET","NUM_FUNCIONARIOS","ID_ALIMENTACAO")

infra2013 <- escolas2013[,ItensInfra]

infra2013PE <- subset(infra2013, SIGLA=="PE" & ID_DEPENDENCIA_ADM < 4)

infra2013PE[is.na(infra2013PE)] <- 0

pontuacaoEscolas <- transform(infra2013PE, prod=20*ID_SALA_PROFESSOR+50*ID_LABORATORIO_INFORMATICA+40*ID_LABORATORIO_CIENCIAS+
                                50*ID_QUADRA_ESPORTES_COBERTA+25*ID_QUADRA_ESPORTES_DESCOBERTA+20*ID_COZINHA+40*ID_BIBLIOTECA+
                                25*ID_AUDITORIO+30*ID_PATIO_COBERTO+15*ID_PATIO_DESCOBERTO+5*NUM_SALAS_EXISTENTES+3*NUM_EQUIP_TV+
                                10*NUM_EQUIP_COPIADORA+5*NUM_EQUIP_IMPRESSORA+10*NUM_EQUIP_SOM+4*NUM_EQUIP_MULTIMIDIA+3*NUM_COMPUTADORES+
                                5*NUM_COMP_ADMINISTRATIVOS+3*NUM_COMP_ALUNOS+20*ID_INTERNET+10*NUM_FUNCIONARIOS+40*ID_ALIMENTACAO )

pontuacaoEscolas <- pontuacaoEscolas[,c("FK_COD_MUNICIPIO","prod")]

PontEscolasPorCidade <- aggregate(pontuacaoEscolas$prod, by=list(CODMUNIC=pontuacaoEscolas$FK_COD_MUNICIPIO), FUN=sum)

names(PontEscolasPorCidade)[names(PontEscolasPorCidade) == 'x'] <- 'PONTUACAO_POR_CIDADE'


#Geracao do grafico
shp <- readOGR("/home/jrocha/Documentos/rStudio/geo", "26MUE250GC_SIR", stringsAsFactors=FALSE, encoding="UTF-8", verbose = FALSE)
shp$CD_GEOCODM <- as.numeric(as.character(shp$CD_GEOCODM))

dados_completos <- merge(shp,PontEscolasPorCidade, by.x = "CD_GEOCODM", by.y = "CODMUNIC")
qpal <- colorQuantile("Blues", dados_completos$PONTUACAO_POR_CIDADE, n = 4)

mapPE <- leaflet() %>% addTiles() %>% addPolygons(data=dados_completos,stroke = FALSE, 
                     fillColor = ~qpal(dados_completos$PONTUACAO_POR_CIDADE), 
                     smoothFactor = 0.2,fillOpacity = 1) %>%  addLegend("bottomright", 
                     pal = qpal, values = dados_completos$PONTUACAO_POR_CIDADE, 
                     title = "PONTOS ESCOLAS POR MUNICIPIO DE PE", opacity = 1)
mapPE

