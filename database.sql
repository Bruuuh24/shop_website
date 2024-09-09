/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 90001 (9.0.1)
 Source Host           : localhost:3306
 Source Schema         : nicsok_assessment

 Target Server Type    : MySQL
 Target Server Version : 90001 (9.0.1)
 File Encoding         : 65001

 Date: 09/09/2024 16:57:30
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
-- Table structure for cart
-- ----------------------------
DROP TABLE IF EXISTS `cart`;
CREATE TABLE `cart`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `product_id` int NOT NULL,
  `product` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `price` decimal(10, 2) NOT NULL,
  `quantity` int NOT NULL,
  PRIMARY KEY (`id` DESC) USING BTREE,
  INDEX `product_id`(`product_id` ASC) USING BTREE,
  INDEX `idx_cart_username`(`user` ASC) USING BTREE,
  CONSTRAINT `product_id` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `user` FOREIGN KEY (`user`) REFERENCES `users` (`username`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 18 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of cart
-- ----------------------------
BEGIN;
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
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `benfits` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of products
-- ----------------------------
BEGIN;
INSERT INTO `products` (`id`, `product`, `price`, `product_type`, `description`, `benfits`) VALUES (1, 'Basic', 10.00, 'vpn', 'Secure your internet with essential protection. Enjoy anonymous browsing and access to basic VPN features.', 'Basic encryption, Unlimited bandwidth, Access to standard servers, Anonymous browsing'), (2, 'Premium ', 30.00, 'vpn', 'Upgrade to premium for enhanced security and performance. Includes faster speeds and access to a wider range of servers.', 'Advanced encryption, Faster connection speeds, Access to global servers, Enhanced privacy features'), (3, 'Maximum ', 50.00, 'vpn', 'Get top-tier security and performance with the maximum plan. Features premium support and advanced security tools.', 'Military-grade encryption, Ultra-fast speeds, Access to all servers, Priority customer support'), (4, 'Group', 50.00, 'vpn', 'Secure your entire team with the group plan. Ideal for families or small businesses needing comprehensive protection.', 'Group account management, Shared VPN access, Centralized billing, Customizable security settings');
COMMIT;

-- ----------------------------
-- Table structure for products_sold
-- ----------------------------
DROP TABLE IF EXISTS `products_sold`;
CREATE TABLE `products_sold`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `product` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `date` timestamp NOT NULL ON UPDATE CURRENT_TIMESTAMP,
  `duration` datetime NOT NULL,
  `quantity` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of products_sold
-- ----------------------------
BEGIN;
INSERT INTO `products_sold` (`id`, `user`, `product`, `date`, `duration`, `quantity`) VALUES (1, 'test', 'Maximum ', '2024-09-07 18:13:13', '2024-10-07 18:13:13', '1'), (2, 'test2', 'Premium ', '2024-09-08 06:54:00', '2024-10-08 06:54:00', '1'), (3, 'test2', 'Group', '2024-09-08 06:57:34', '2024-10-08 06:57:34', '1'), (4, 'test2', 'Premium', '2024-09-08 07:04:14', '2024-10-08 07:02:09', '1'), (5, 'test2', 'Basic', '2024-09-08 07:06:22', '2024-10-08 07:06:22', '1'), (6, 'test2', 'Maximum ', '2024-09-08 07:06:22', '2024-10-08 07:06:22', '1'), (8, 'test2', 'Basic', '2024-09-08 16:03:10', '2024-10-08 16:03:10', '1');
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
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `id`(`account_type` ASC) USING BTREE,
  INDEX `username`(`username` ASC) USING BTREE,
  UNIQUE INDEX `username_2`(`username` ASC) USING BTREE,
  INDEX `idx_username`(`username` ASC) USING BTREE,
  CONSTRAINT `id` FOREIGN KEY (`account_type`) REFERENCES `account_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 21 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of users
-- ----------------------------
BEGIN;
INSERT INTO `users` (`id`, `username`, `password`, `account_type`) VALUES (1, 'test', '50c0152c2952082aeaf427885a2f617d67cf6de183a8816c0955ea5b875a216b', 1), (2, 'test2', '50c0152c2952082aeaf427885a2f617d67cf6de183a8816c0955ea5b875a216b', 2), (13, 'test3', 'b819462a81cd04dbabfe87db6bb30678baaaa74cc078a6d219b13aeb4c579ece', 1), (14, 'test4', 'eefefd2b42ee468b46da4597e68fd6f69d89b0caeca05ca96b5014abef6b5cdd', 1), (15, 'test5', '2e0b8d61fa2a6959d254b6ff5d0fb512249329097336a35568089933b49abdde', 1), (16, 'test6 ', 'e81dfe69841ad2f7b5790b63e998f0febaf3b29acd732881975130761b98e2c7', 1), (17, 'test7', '50c0152c2952082aeaf427885a2f617d67cf6de183a8816c0955ea5b875a216b', 1), (18, 'test8', '50c0152c2952082aeaf427885a2f617d67cf6de183a8816c0955ea5b875a216b', 1), (19, 'test9', '50c0152c2952082aeaf427885a2f617d67cf6de183a8816c0955ea5b875a216b', 1), (20, 'test10', '50c0152c2952082aeaf427885a2f617d67cf6de183a8816c0955ea5b875a216b', 1);
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
