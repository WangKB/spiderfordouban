CREATE DATABASE  IF NOT EXISTS `douban` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `douban`;
-- MySQL dump 10.13  Distrib 5.7.12, for Win64 (x86_64)
--
-- Host: localhost    Database: douban
-- ------------------------------------------------------
-- Server version	5.7.17-log

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
-- Table structure for table `actor_subject`
--

DROP TABLE IF EXISTS `actor_subject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `actor_subject` (
  `a_id` int(11) NOT NULL,
  `s_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `actor_subject`
--

LOCK TABLES `actor_subject` WRITE;
/*!40000 ALTER TABLE `actor_subject` DISABLE KEYS */;
/*!40000 ALTER TABLE `actor_subject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `celebrity`
--

DROP TABLE IF EXISTS `celebrity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `celebrity` (
  `id` int(11) NOT NULL,
  `zodiac` varchar(255) DEFAULT NULL,
  `birthday` varchar(255) DEFAULT NULL,
  `birthplace` varchar(255) DEFAULT NULL,
  `profession` varchar(255) DEFAULT NULL,
  `for_lang_names` varchar(2000) DEFAULT NULL,
  `name` varchar(2000) DEFAULT NULL,
  `photo` varchar(2000) DEFAULT NULL,
  `gender` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `celebrity`
--

LOCK TABLES `celebrity` WRITE;
/*!40000 ALTER TABLE `celebrity` DISABLE KEYS */;
/*!40000 ALTER TABLE `celebrity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `director_subject`
--

DROP TABLE IF EXISTS `director_subject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `director_subject` (
  `d_id` int(11) NOT NULL,
  `s_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `director_subject`
--

LOCK TABLES `director_subject` WRITE;
/*!40000 ALTER TABLE `director_subject` DISABLE KEYS */;
/*!40000 ALTER TABLE `director_subject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `screenwriter_subject`
--

DROP TABLE IF EXISTS `screenwriter_subject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `screenwriter_subject` (
  `sw_id` int(11) NOT NULL,
  `s_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `screenwriter_subject`
--

LOCK TABLES `screenwriter_subject` WRITE;
/*!40000 ALTER TABLE `screenwriter_subject` DISABLE KEYS */;
/*!40000 ALTER TABLE `screenwriter_subject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subject`
--

DROP TABLE IF EXISTS `subject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `subject` (
  `id` int(11) NOT NULL,
  `title` varchar(2000) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `product_nation` varchar(255) DEFAULT NULL,
  `language` varchar(255) DEFAULT NULL,
  `premiere` varchar(2000) DEFAULT NULL,
  `duration` float DEFAULT NULL,
  `rating_num` float DEFAULT NULL,
  `rating_people` int(11) DEFAULT NULL,
  `periods` int(11) DEFAULT NULL,
  `period_duration` varchar(255) DEFAULT NULL,
  `photo` varchar(2000) DEFAULT NULL,
  `year` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subject`
--

LOCK TABLES `subject` WRITE;
/*!40000 ALTER TABLE `subject` DISABLE KEYS */;
/*!40000 ALTER TABLE `subject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `task`
--

DROP TABLE IF EXISTS `task`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `task` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(2000) DEFAULT NULL,
  `isScanned` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task`
--

LOCK TABLES `task` WRITE;
/*!40000 ALTER TABLE `task` DISABLE KEYS */;
/*!40000 ALTER TABLE `task` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `year_tag`
--

DROP TABLE IF EXISTS `year_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `year_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `year` varchar(2000) DEFAULT NULL,
  `page` int(11) DEFAULT NULL,
  `isScanned` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `year_tag`
--

LOCK TABLES `year_tag` WRITE;
/*!40000 ALTER TABLE `year_tag` DISABLE KEYS */;
/*!40000 ALTER TABLE `year_tag` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-03-27 21:31:08
