/*
 Navicat Premium Data Transfer

 Source Server         : 192.168.123.180stock_db
 Source Server Type    : MySQL
 Source Server Version : 100126
 Source Host           : www.hlaijia.com:13306
 Source Schema         : stock_db

 Target Server Type    : MySQL
 Target Server Version : 100126
 File Encoding         : 65001

 Date: 16/01/2020 17:38:08
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for message
-- ----------------------------
DROP TABLE IF EXISTS `message`;
CREATE TABLE `message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `from_id` varchar(255) DEFAULT NULL,
  `from_name` varchar(255) DEFAULT NULL,
  `from_member_wxid` varchar(255) DEFAULT NULL,
  `to_id` varchar(255) DEFAULT NULL,
  `to_name` varchar(255) DEFAULT NULL,
  `content` text,
  `creat_time` datetime DEFAULT NULL,
  `state` int(2) DEFAULT NULL COMMENT '0：未处理1：已处理',
  `send_or_recv` tinyint(255) DEFAULT NULL COMMENT '1:发送0：接收',
  `msg_type` varchar(128) DEFAULT NULL COMMENT '消息类型',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=166 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for monitor_data
-- ----------------------------
DROP TABLE IF EXISTS `monitor_data`;
CREATE TABLE `monitor_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(64) NOT NULL,
  `date` varchar(64) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `ext_data` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for strategy_conf
-- ----------------------------
DROP TABLE IF EXISTS `strategy_conf`;
CREATE TABLE `strategy_conf` (
  `id` int(11) NOT NULL,
  `createid` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `strategy_sql` text,
  `create_time` datetime DEFAULT NULL,
  `cron` varchar(128) DEFAULT NULL,
  `toid` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for tick_conf
-- ----------------------------
DROP TABLE IF EXISTS `tick_conf`;
CREATE TABLE `tick_conf` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `industry` varchar(255) DEFAULT NULL,
  `code` varchar(64) NOT NULL,
  `create_time` datetime NOT NULL,
  `remark` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=3778 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for tick_data
-- ----------------------------
DROP TABLE IF EXISTS `tick_data`;
CREATE TABLE `tick_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` varchar(64) DEFAULT NULL,
  `code` varchar(64) DEFAULT NULL,
  `open` double DEFAULT NULL,
  `high` double DEFAULT NULL,
  `close` double DEFAULT NULL,
  `low` double DEFAULT NULL,
  `volume` double DEFAULT NULL,
  `price_change` double DEFAULT NULL,
  `p_change` double DEFAULT NULL,
  `ma5` double DEFAULT NULL,
  `ma10` double DEFAULT NULL,
  `ma20` double DEFAULT NULL,
  `v_ma5` double DEFAULT NULL,
  `v_ma10` double DEFAULT NULL,
  `v_ma20` double DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `pk_code_date` (`date`,`code`),
  FULLTEXT KEY `idx_code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=541871 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for trade_cal
-- ----------------------------
DROP TABLE IF EXISTS `trade_cal`;
CREATE TABLE `trade_cal` (
  `index` bigint(20) DEFAULT NULL,
  `exchange` text,
  `cal_date` text,
  `is_open` bigint(20) DEFAULT NULL,
  KEY `ix_trade_cal_index` (`index`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
