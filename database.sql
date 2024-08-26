/*
 Navicat Premium Data Transfer

 Source Server         : local
 Source Server Type    : MySQL
 Source Server Version : 90001 (9.0.1)
 Source Host           : localhost:3306
 Source Schema         : nicsok_assessment

 Target Server Type    : MySQL
 Target Server Version : 90001 (9.0.1)
 File Encoding         : 65001

 Date: 26/08/2024 17:15:03
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for account_type
-- ----------------------------
DROP TABLE IF EXISTS `account_type`;
CREATE TABLE `account_type`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `account_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of account_type
-- ----------------------------
BEGIN;
INSERT INTO `account_type` (`id`, `account_type`) VALUES (1, 'normal'), (2, 'admin');
COMMIT;

-- ----------------------------
-- Table structure for products
-- ----------------------------
DROP TABLE IF EXISTS `products`;
CREATE TABLE `products`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `product` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `price` decimal(10, 2) NOT NULL,
  `product_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `desciption` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `benfits` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of products
-- ----------------------------
BEGIN;
INSERT INTO `products` (`id`, `product`, `price`, `product_type`, `desciption`, `benfits`) VALUES (1, 'Basic', 10.00, 'tier1', '', 'test'), (2, 'Premium ', 30.00, 'tier2', NULL, NULL), (3, 'Maximum ', 50.00, 'tier3', NULL, NULL), (4, 'Group Plan ', 80.00, 'tier4', NULL, NULL);
COMMIT;

-- ----------------------------
-- Table structure for products_bought
-- ----------------------------
DROP TABLE IF EXISTS `products_bought`;
CREATE TABLE `products_bought`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `product` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `date` datetime NULL DEFAULT NULL,
  `amount` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of products_bought
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `account_type` int NOT NULL,
  PRIMARY KEY (`id`, `username`, `password`, `account_type`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 17 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of users
-- ----------------------------
BEGIN;
INSERT INTO `users` (`id`, `username`, `password`, `account_type`) VALUES (1, 'test', '50c0152c2952082aeaf427885a2f617d67cf6de183a8816c0955ea5b875a216b', 1), (2, 'test2', '50c0152c2952082aeaf427885a2f617d67cf6de183a8816c0955ea5b875a216b', 2), (13, 'test3', 'b819462a81cd04dbabfe87db6bb30678baaaa74cc078a6d219b13aeb4c579ece', 1), (14, 'test4', 'eefefd2b42ee468b46da4597e68fd6f69d89b0caeca05ca96b5014abef6b5cdd', 1), (15, 'test5', '2e0b8d61fa2a6959d254b6ff5d0fb512249329097336a35568089933b49abdde', 1), (16, 'test6 ', 'e81dfe69841ad2f7b5790b63e998f0febaf3b29acd732881975130761b98e2c7', 1);
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
