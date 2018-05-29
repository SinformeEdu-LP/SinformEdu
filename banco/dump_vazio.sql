-- MySQL dump 10.13  Distrib 5.7.20, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: sinformedb
-- ------------------------------------------------------
-- Server version	5.5.5-10.1.25-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `convenio`
--


CREATE Database `sinformedb`;

USE `sinformedb`;


DROP TABLE IF EXISTS `convenio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `convenio` (
  `NR_CONVENIO` bigint(20) NOT NULL,
  `ID_PROPOSTA` bigint(20) DEFAULT NULL,
  `DIA` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `MES` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ANO` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `DIA_ASSIN_CONV` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `SIT_CONVENIO` varchar(300) COLLATE utf8_unicode_ci DEFAULT NULL,
  `SITUACAO_PUBLICACAO` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `SUBSITUACAO_CONV` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `INSTRUMENTO_ATIVO` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `IND_OPERA_OBTV` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `DIA_PUBL_CONV` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `DATA_INICIO_VIGENC_CONV` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `DATA_FIM_VIGENC_CONV` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `DIAS_PREST_CONTAS` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `DATA_LIMITE_PREST_CONTAS` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `SITUACAO_CONTRATACAO` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `QTDE_CONVENIOS` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `QTD_TA` int(11) DEFAULT NULL,
  `QTD_PRORROGA` int(11) DEFAULT NULL,
  `VL_GLOBAL_CONV` double DEFAULT NULL,
  `VL_REPASSE_CONV` double DEFAULT NULL,
  `VL_CONTRAPARTIDA_CONV` double DEFAULT NULL,
  `VL_EMPENHADO_CONV` double DEFAULT NULL,
  `VL_DESEMBOLSADO_CONV` double DEFAULT NULL,
  `VL_SALDO_REMAN_TESOURO` double DEFAULT NULL,
  `VL_SALDO_REMAN_CONVENENTE` double DEFAULT NULL,
  `VL_RENDIMENTO_APLICACAO` double DEFAULT NULL,
  `VL_INGRESSO_CONTRAPARTIDA` double DEFAULT NULL,
  PRIMARY KEY (`NR_CONVENIO`),
  KEY `ID_PROPOSTA_idx` (`ID_PROPOSTA`),
  CONSTRAINT `ID_PROPOSTA_CONV` FOREIGN KEY (`ID_PROPOSTA`) REFERENCES `proposta` (`ID_PROPOSTA`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary table structure for view `convenio_pagamentos`
--

DROP TABLE IF EXISTS `convenio_pagamentos`;
/*!50001 DROP VIEW IF EXISTS `convenio_pagamentos`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `convenio_pagamentos` AS SELECT 
 1 AS `NR_CONVENIO`,
 1 AS `ID_PROPOSTA`,
 1 AS `DIA_ASSIN_CONV`,
 1 AS `VL_GLOBAL_CONV`,
 1 AS `total`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `desembolso`
--

DROP TABLE IF EXISTS `desembolso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `desembolso` (
  `NR_CONVENIO` bigint(20) NOT NULL,
  `DT_ULT_DESEMBOLSO` date DEFAULT NULL,
  `QTD_DIAS_SEM_DESEMBOLSO` int(11) DEFAULT NULL,
  `DATA_DESEMBOLSO` date DEFAULT NULL,
  `NR_SIAFI` varchar(12) COLLATE utf8_unicode_ci DEFAULT NULL,
  `VL_DESEMBOLSADO` double DEFAULT NULL,
  `ID` bigint(20) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`ID`),
  KEY `NR_CONVENIO_DESEMBOLSO` (`NR_CONVENIO`),
  CONSTRAINT `NR_CONVENIO_DESEMBOLSO` FOREIGN KEY (`NR_CONVENIO`) REFERENCES `convenio` (`NR_CONVENIO`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=211479 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `emenda`
--

DROP TABLE IF EXISTS `emenda`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `emenda` (
  `ID_PROPOSTA` bigint(20) NOT NULL,
  `ID_PARLAMENTAR` int(11) NOT NULL,
  `NR_EMENDA` int(11) DEFAULT NULL,
  `BENEFICIARIO_EMENDA` bigint(20) DEFAULT NULL,
  `IND_IMPOSITIVO` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `VL_REPASSE_PROPOSTA_EMENDA` double DEFAULT NULL,
  `VL_REPASSE_EMENDA` double DEFAULT NULL,
  PRIMARY KEY (`ID_PROPOSTA`,`ID_PARLAMENTAR`),
  KEY `CNPJ PROPONENTE_idx` (`BENEFICIARIO_EMENDA`),
  KEY `NOME_PARLAMENTAR_PROPOSTA_idx` (`ID_PARLAMENTAR`),
  CONSTRAINT `CNPJ_PROPONENTE` FOREIGN KEY (`BENEFICIARIO_EMENDA`) REFERENCES `proponente` (`IDENTIF_PROPONENTE`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `ID_PROPOSTA_EMENDA` FOREIGN KEY (`ID_PROPOSTA`) REFERENCES `proposta` (`ID_PROPOSTA`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `NOME_PARLAMENTAR_PROPOSTA` FOREIGN KEY (`ID_PARLAMENTAR`) REFERENCES `parlamentar` (`ID_PARLAMENTAR`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `empenho`
--

DROP TABLE IF EXISTS `empenho`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `empenho` (
  `NR_EMPENHO` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `NR_CONVENIO` bigint(20) NOT NULL,
  `TIPO_NOTA` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `DESC_TIPO_NOTA` text COLLATE utf8_unicode_ci,
  `DATA_EMISSAO` date DEFAULT NULL,
  `COD_SITUACAO_EMPENHO` int(11) DEFAULT NULL,
  `DESC_SITUACAO_EMPENHO` text COLLATE utf8_unicode_ci,
  `VALOR_EMPENHO` double DEFAULT NULL,
  `ID_EMPENHO` bigint(20) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`ID_EMPENHO`),
  KEY `NR_CONVENIO_idx` (`NR_CONVENIO`),
  CONSTRAINT `NR_CONVENIO` FOREIGN KEY (`NR_CONVENIO`) REFERENCES `convenio` (`NR_CONVENIO`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=188377 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fornecedor`
--

DROP TABLE IF EXISTS `fornecedor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fornecedor` (
  `IDENTIF_FORNECEDOR` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `NM_FORNECEDOR` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`IDENTIF_FORNECEDOR`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `historico_situacao`
--

DROP TABLE IF EXISTS `historico_situacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `historico_situacao` (
  `ID_PROPOSTA` bigint(20) NOT NULL,
  `NR_CONVENIO` bigint(20) NOT NULL,
  `DIA_HISTORICO_SIT` date DEFAULT NULL,
  `HISTORICO_SIT` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `DIAS_HISTORICO_SIT` int(11) DEFAULT NULL,
  `COD_HISTORICO_SIT` bigint(20) DEFAULT NULL,
  `ID_HISTORICO_SIT` bigint(20) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`ID_HISTORICO_SIT`),
  KEY `NR_CONVENIO_idx` (`NR_CONVENIO`),
  KEY `ID_PROPOSTA_HIST` (`ID_PROPOSTA`),
  CONSTRAINT `ID_PROPOSTA_HIST` FOREIGN KEY (`ID_PROPOSTA`) REFERENCES `proposta` (`ID_PROPOSTA`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `NR_CONVENIO_HIST` FOREIGN KEY (`NR_CONVENIO`) REFERENCES `convenio` (`NR_CONVENIO`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `meta`
--

DROP TABLE IF EXISTS `meta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `meta` (
  `ID_META` bigint(20) NOT NULL,
  `NR_CONVENIO` bigint(20) DEFAULT NULL,
  `NR_META` bigint(20) DEFAULT NULL,
  `TIPO_META` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `DESC_META` text COLLATE utf8_unicode_ci,
  `DATA_INICIO_META` date DEFAULT NULL,
  `DATA_FIM_META` date DEFAULT NULL,
  `UF_META` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `MUNIC_META` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ENDERECO_META` text COLLATE utf8_unicode_ci,
  `CEP_META` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `QTD_META` bigint(20) DEFAULT NULL,
  `UND_FORNECIMENTO_META` text COLLATE utf8_unicode_ci,
  `VL_META` double DEFAULT NULL,
  PRIMARY KEY (`ID_META`),
  KEY `NR_CONVENIO_idx` (`NR_CONVENIO`),
  CONSTRAINT `NR_CONVENIO_META` FOREIGN KEY (`NR_CONVENIO`) REFERENCES `convenio` (`NR_CONVENIO`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `municipio`
--

DROP TABLE IF EXISTS `municipio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `municipio` (
  `COD_MUNIC_IBGE` bigint(20) NOT NULL,
  `MUNIC_PROPONENTE` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `UF_PROPONENTE` varchar(2) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`COD_MUNIC_IBGE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `obtv_convenente`
--

DROP TABLE IF EXISTS `obtv_convenente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `obtv_convenente` (
  `NR_MOV_FIN` bigint(20) NOT NULL,
  `IDENTIF_FAVORECIDO_OBTV_CONV` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `TP_AQUISICAO` text COLLATE utf8_unicode_ci,
  `VL_PAGO_OBTV_CONV` double DEFAULT NULL,
  `NM_FAVORECIDO_OBTV_CONV` text COLLATE utf8_unicode_ci,
  `ID_OBTV_CONV` bigint(20) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`ID_OBTV_CONV`),
  KEY `NR_MOV_FIN_OBTV_idx` (`NR_MOV_FIN`),
  CONSTRAINT `NR_MOV_FIN_OBTV` FOREIGN KEY (`NR_MOV_FIN`) REFERENCES `pagamento` (`NR_MOV_FIN`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=1267285 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `orgao`
--

DROP TABLE IF EXISTS `orgao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `orgao` (
  `COD_ORGAO` bigint(20) NOT NULL,
  `DESC_ORGAO` text COLLATE utf8_unicode_ci,
  PRIMARY KEY (`COD_ORGAO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pagamento`
--

DROP TABLE IF EXISTS `pagamento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pagamento` (
  `NR_MOV_FIN` bigint(20) NOT NULL,
  `NR_CONVENIO` bigint(20) DEFAULT NULL,
  `IDENTIF_FORNECEDOR` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `TP_MOV_FIN` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `DATA_PAG` date DEFAULT NULL,
  `VL_PAGO` double DEFAULT NULL,
  `NR_DL` text COLLATE utf8_unicode_ci,
  `DESC_DL` text COLLATE utf8_unicode_ci,
  PRIMARY KEY (`NR_MOV_FIN`),
  KEY `NR_CONVENIO_idx` (`NR_CONVENIO`),
  KEY `IDENTIF_FORNECEDOR_idx` (`IDENTIF_FORNECEDOR`),
  CONSTRAINT `IDENTIF_FORNECEDOR` FOREIGN KEY (`IDENTIF_FORNECEDOR`) REFERENCES `fornecedor` (`IDENTIF_FORNECEDOR`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `NR_CONVENIO_PAGAMENTO` FOREIGN KEY (`NR_CONVENIO`) REFERENCES `convenio` (`NR_CONVENIO`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `parlamentar`
--

DROP TABLE IF EXISTS `parlamentar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `parlamentar` (
  `NOME_PARLAMENTAR` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `TIPO_PARLAMENTAR` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `NOME_COMPLETO` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `SIGLA_PARTIDO` varchar(12) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ID_PARLAMENTAR` int(11) NOT NULL AUTO_INCREMENT,
  `FUNCAO` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`ID_PARLAMENTAR`)
) ENGINE=InnoDB AUTO_INCREMENT=595 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary table structure for view `parlamentares`
--

DROP TABLE IF EXISTS `parlamentares`;
/*!50001 DROP VIEW IF EXISTS `parlamentares`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `parlamentares` AS SELECT 
 1 AS `ID_PARLAMENTAR`,
 1 AS `NOME_PARLAMENTAR`,
 1 AS `ID_PROPOSTA`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `proponente`
--

DROP TABLE IF EXISTS `proponente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `proponente` (
  `IDENTIF_PROPONENTE` bigint(20) NOT NULL,
  `UF_PROPONENTE` varchar(2) COLLATE utf8_unicode_ci DEFAULT NULL,
  `MUNIC_PROPONENTE` varchar(300) COLLATE utf8_unicode_ci DEFAULT NULL,
  `NATUREZA_JURIDICA` varchar(300) COLLATE utf8_unicode_ci DEFAULT NULL,
  `NM_PROPONENTE` varchar(300) COLLATE utf8_unicode_ci DEFAULT NULL,
  `CEP_PROPONENTE` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ENDERECO_PROPONENTE` text COLLATE utf8_unicode_ci,
  `BAIRRO_PROPONENTE` varchar(300) COLLATE utf8_unicode_ci DEFAULT NULL,
  `COD_MUNIC_IBGE` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`IDENTIF_PROPONENTE`),
  KEY `fk_proponente_municipio1_idx` (`COD_MUNIC_IBGE`),
  CONSTRAINT `fk_proponente_municipio1` FOREIGN KEY (`COD_MUNIC_IBGE`) REFERENCES `municipio` (`COD_MUNIC_IBGE`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `proposta`
--

DROP TABLE IF EXISTS `proposta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `proposta` (
  `ID_PROPOSTA` bigint(20) NOT NULL,
  `NR_PROPOSTA` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `IDENTIF_PROPONENTE` bigint(20) DEFAULT NULL,
  `DIA_PROPOSTA` date DEFAULT NULL,
  `MODALIDADE` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `SIT_PROPOSTA` varchar(300) COLLATE utf8_unicode_ci DEFAULT NULL,
  `DIA_INIC_VIGENCIA_PROPOSTA` date DEFAULT NULL,
  `DIA_FIM_VIGENCIA_PROPOSTA` date DEFAULT NULL,
  `OBJETO_PROPOSTA` text COLLATE utf8_unicode_ci,
  `VL_GLOBAL_PROP` double DEFAULT NULL,
  `VL_REPASSE_PROP` double DEFAULT NULL,
  `VL_CONTRAPARTIDA_PROP` double DEFAULT NULL,
  `COD_ORGAO_SUP` bigint(20) DEFAULT NULL,
  `COD_ORGAO` bigint(20) DEFAULT NULL,
  `NM_BANCO` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `SITUACAO_CONTA` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `SITUACAO_PROJETO_BASICO` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`ID_PROPOSTA`),
  KEY `IDENTIF_PROPONENTE_idx` (`IDENTIF_PROPONENTE`),
  KEY `COD_ORGAO_idx` (`COD_ORGAO`),
  KEY `COD_ORGAO_SUP` (`COD_ORGAO_SUP`),
  CONSTRAINT `COD_ORGAO` FOREIGN KEY (`COD_ORGAO`) REFERENCES `orgao` (`COD_ORGAO`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `IDENTIF_PROPONENTE` FOREIGN KEY (`IDENTIF_PROPONENTE`) REFERENCES `proponente` (`IDENTIF_PROPONENTE`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary table structure for view `soma_pagamentos`
--

DROP TABLE IF EXISTS `soma_pagamentos`;
/*!50001 DROP VIEW IF EXISTS `soma_pagamentos`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `soma_pagamentos` AS SELECT 
 1 AS `NR_CONVENIO`,
 1 AS `total`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `termo_aditivo`
--

DROP TABLE IF EXISTS `termo_aditivo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `termo_aditivo` (
  `NR_CONVENIO` bigint(20) NOT NULL,
  `NUMERO_TA` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `TIPO_TA` varchar(300) COLLATE utf8_unicode_ci DEFAULT NULL,
  `VL_GLOBAL_TA` double DEFAULT NULL,
  `VL_REPASSE_TA` double DEFAULT NULL,
  `VL_CONTRAPARTIDA_TA` double DEFAULT NULL,
  `DT_ASSINATURA_TA` date DEFAULT NULL,
  `DT_INICIO_TA` date DEFAULT NULL,
  `DT_FIM_TA` date DEFAULT NULL,
  `JUSTIFICATIVA_TA` text COLLATE utf8_unicode_ci,
  `ID_TA` bigint(20) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`ID_TA`),
  KEY `NR_CONVENIO_idx` (`NR_CONVENIO`),
  CONSTRAINT `NR_CONVENIO_TA` FOREIGN KEY (`NR_CONVENIO`) REFERENCES `convenio` (`NR_CONVENIO`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=212063 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Final view structure for view `convenio_pagamentos`
--

/*!50001 DROP VIEW IF EXISTS `convenio_pagamentos`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8_unicode_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `convenio_pagamentos` AS select `c`.`NR_CONVENIO` AS `NR_CONVENIO`,`c`.`ID_PROPOSTA` AS `ID_PROPOSTA`,`c`.`DIA_ASSIN_CONV` AS `DIA_ASSIN_CONV`,`c`.`VL_GLOBAL_CONV` AS `VL_GLOBAL_CONV`,`s`.`total` AS `total` from (`convenio` `c` join `soma_pagamentos` `s`) where (`c`.`NR_CONVENIO` = `s`.`NR_CONVENIO`) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `parlamentares`
--

/*!50001 DROP VIEW IF EXISTS `parlamentares`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8_unicode_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `parlamentares` AS select `p`.`ID_PARLAMENTAR` AS `ID_PARLAMENTAR`,`p`.`NOME_PARLAMENTAR` AS `NOME_PARLAMENTAR`,`e`.`ID_PROPOSTA` AS `ID_PROPOSTA` from (`parlamentar` `p` join `emenda` `e`) where (`p`.`ID_PARLAMENTAR` = `e`.`ID_PARLAMENTAR`) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `soma_pagamentos`
--

/*!50001 DROP VIEW IF EXISTS `soma_pagamentos`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `soma_pagamentos` AS select `pagamento`.`NR_CONVENIO` AS `NR_CONVENIO`,sum(`pagamento`.`VL_PAGO`) AS `total` from `pagamento` group by `pagamento`.`NR_CONVENIO` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-01-28 23:48:12
