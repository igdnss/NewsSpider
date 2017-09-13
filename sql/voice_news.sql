/*
SQLyog Ultimate v11.25 (64 bit)
MySQL - 5.6.29 : Database - voice_news
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`voice_news` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `voice_news`;

/*Table structure for table `news_info_tbl` */

CREATE TABLE `news_info_tbl` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rawPath` varchar(100) DEFAULT NULL COMMENT '原始新闻的本地路径',
  `absPath` varchar(100) DEFAULT NULL COMMENT '新闻摘要文本的本地路径',
  `voicePath` varchar(100) DEFAULT NULL COMMENT '新闻摘要语音的本地路径',
  `deployTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '新闻页上显示的时间',
  `crawlTime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '新闻爬取时间',
  `hot` int(11) DEFAULT NULL COMMENT '新闻的热度，是点击率和评论数的函数',
  `hotUpdateTime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '热度更新时间',
  `url` varchar(200) DEFAULT NULL COMMENT '新闻页的远程地址',
  `title` varchar(100) DEFAULT NULL COMMENT '新闻标题',
  `isIdle` tinyint(4) DEFAULT NULL COMMENT '废弃标记',
  `state` int(11) DEFAULT '1' COMMENT '新闻在系统中的状态（1：preprocessed，2: extracted，3: integered，4: deployed）',
  `type` varchar(50) DEFAULT NULL COMMENT '新闻类型',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=199 DEFAULT CHARSET=utf8;

/*Data for the table `news_info_tbl` */

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
