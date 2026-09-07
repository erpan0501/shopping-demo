-- 仅供智能客服联调的脱敏演示数据：FAQ、订单、物流及订单商品。
-- 完整商城功能需要在本目录另行放入经审核的本地数据库导出文件。
SET NAMES utf8mb4;
USE `travel`;

CREATE TABLE IF NOT EXISTS `bz_orders` (
  `id` varchar(50) NOT NULL,
  `payment` decimal(20,2) DEFAULT NULL,
  `paymentType` varchar(1) DEFAULT NULL,
  `postFee` varchar(50) DEFAULT NULL,
  `status` varchar(1) DEFAULT NULL,
  `createTime` datetime DEFAULT NULL,
  `paymentTime` datetime DEFAULT NULL,
  `consignTime` datetime DEFAULT NULL,
  `endTime` datetime DEFAULT NULL,
  `closeTime` datetime DEFAULT NULL,
  `shippingName` varchar(20) DEFAULT NULL,
  `shippingCode` varchar(20) DEFAULT NULL,
  `userId` bigint DEFAULT NULL,
  `buyerMessage` varchar(100) DEFAULT NULL,
  `buyerNick` varchar(50) DEFAULT NULL,
  `receiverAreaName` varchar(255) DEFAULT NULL,
  `receiverMobile` varchar(12) DEFAULT NULL,
  `receiverZipCode` varchar(15) DEFAULT NULL,
  `receiver` varchar(50) DEFAULT NULL,
  `expire` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_bz_orders_user_status` (`userId`, `status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `bz_cart_goods` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `goodId` bigint DEFAULT NULL,
  `goodsName` varchar(255) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `headerPic` varchar(255) DEFAULT NULL,
  `num` int DEFAULT NULL,
  `orderId` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_bz_cart_goods_order` (`orderId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Java 应用启动时会读取该表加载敏感词词库；演示环境保持为空即可。
CREATE TABLE IF NOT EXISTS `bz_sensitive_word` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `word` varchar(255) NOT NULL,
  `type` varchar(16) DEFAULT 'deny',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `bz_shopping_user` (
  `id` bigint NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `nickName` varchar(50) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `status` varchar(1) DEFAULT NULL,
  `headPic` varchar(150) DEFAULT NULL,
  `sex` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_bz_shopping_user_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 仅为 JWT 联调准备的固定演示用户；不代表生产账号，也不包含真实个人信息。
INSERT INTO `bz_shopping_user`
  (`id`, `username`, `password`, `phone`, `nickName`, `status`)
VALUES
  (1, 'agent_demo', '80626b8d488c4ebe554746a09ca115c3', '13900000000', '演示用户', 'Y')
ON DUPLICATE KEY UPDATE `status` = VALUES(`status`);

INSERT INTO `bz_orders`
  (`id`, `payment`, `paymentType`, `postFee`, `status`, `createTime`, `paymentTime`, `consignTime`, `shippingName`, `shippingCode`, `userId`, `buyerNick`)
VALUES
  ('2087106115733889025', 199.00, '1', '0.00', '4', '2026-08-20 10:00:00', '2026-08-20 10:01:00', '2026-08-21 09:30:00', '顺丰速运', 'SF1234567890', 1, '演示用户'),
  ('2087106115733889026', 89.00, '2', '0.00', '3', '2026-08-22 11:00:00', '2026-08-22 11:01:00', NULL, NULL, NULL, 1, '演示用户'),
  ('2087106115733889027', 56.00, '1', '0.00', '1', '2026-08-23 12:00:00', NULL, NULL, NULL, NULL, 1, '演示用户'),
  ('2087106115733889028', 129.00, '2', '0.00', '5', '2026-08-10 15:00:00', '2026-08-10 15:02:00', '2026-08-11 09:00:00', '中通快递', 'ZT9876543210', 1, '演示用户')
ON DUPLICATE KEY UPDATE `status` = VALUES(`status`);

INSERT INTO `bz_cart_goods` (`goodId`, `goodsName`, `price`, `num`, `orderId`)
SELECT 10001, '演示商品 A', 199.00, 1, '2087106115733889025'
WHERE NOT EXISTS (SELECT 1 FROM `bz_cart_goods` WHERE `orderId` = '2087106115733889025');
