/*
 Navicat Premium Data Transfer

 Source Server         : school
 Source Server Type    : MySQL
 Source Server Version : 80023
 Source Host           : 10.0.0.17:3306
 Source Schema         : nicsok_assessment

 Target Server Type    : MySQL
 Target Server Version : 80099
 File Encoding         : 65001

 Date: 03/08/2024 11:53:30
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for products
-- ----------------------------
DROP TABLE IF EXISTS `products`;
CREATE TABLE `products`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `product` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `price` decimal(10, 2) NOT NULL,
  `product_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of products
-- ----------------------------
BEGIN;
INSERT INTO `products` (`id`, `product`, `price`, `product_type`) VALUES (1, 'Basic Subscription', 45.00, 'tier_1 '), (2, 'Basic+ Subscription ', 90.00, 'Tier2'), (3, 'Premium Basic Subscription ', 135.00, 'Tier3'), (4, 'Premium Pro Subscription', 180.00, 'Tier4');
COMMIT;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `account_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`, `username`, `password`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of users
-- ----------------------------
BEGIN;
INSERT INTO `users` (`id`, `username`, `password`, `account_type`) VALUES (1, 'test', '50c0152c2952082aeaf427885a2f617d67cf6de183a8816c0955ea5b875a216b', 'normal'), (12, 'test', '50c0152c2952082aeaf427885a2f617d67cf6de183a8816c0955ea5b875a216b', NULL);
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
