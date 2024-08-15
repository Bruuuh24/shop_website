/*
 Navicat Premium Data Transfer

 Source Server         : School
 Source Server Type    : MySQL
 Source Server Version : 80023
 Source Host           : 10.0.0.17:3306
 Source Schema         : nicsok_assessment

 Target Server Type    : MySQL
 Target Server Version : 80023
 File Encoding         : 65001

 Date: 15/08/2024 14:03:39
*/

SET NAMES utf8mb4;
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
  `desciption` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `benfits` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of products
-- ----------------------------
BEGIN;
INSERT INTO `products` (`id`, `product`, `price`, `product_type`, `desciption`, `benfits`) VALUES (1, 'Basic Subscription', 45.00, 'tier_1 ', NULL, NULL), (2, 'Basic+ Subscription ', 90.00, 'Tier2', NULL, NULL), (3, 'Premium Basic Subscription ', 135.00, 'Tier3', NULL, NULL), (4, 'Premium Pro Subscription', 180.00, 'Tier4', NULL, NULL);
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
) ENGINE = InnoDB AUTO_INCREMENT = 15 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of users
-- ----------------------------
BEGIN;
INSERT INTO `users` (`id`, `username`, `password`, `account_type`) VALUES (1, 'test', '50c0152c2952082aeaf427885a2f617d67cf6de183a8816c0955ea5b875a216b', 'normal'), (2, 'test', '50c0152c2952082aeaf427885a2f617d67cf6de183a8816c0955ea5b875a216b', NULL), (13, 'nicholas\' bum', 'b819462a81cd04dbabfe87db6bb30678baaaa74cc078a6d219b13aeb4c579ece', NULL), (14, 's', 'eefefd2b42ee468b46da4597e68fd6f69d89b0caeca05ca96b5014abef6b5cdd', NULL);
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
