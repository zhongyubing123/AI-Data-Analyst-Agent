-- =============================================================
-- 一站式脚本：建库、导入、分层、汇总
-- 用法：
--   1) 把 CSV 路径改成你的实际路径（见 1.2）
--   2) mysql --local-infile=1 --default-character-set=utf8mb4 -u root -p < mysql_all.sql
-- 分层：ODS 原始 → DWD 清洗 → DWS 六个主题
-- =============================================================

CREATE DATABASE IF NOT EXISTS ecommerce
  DEFAULT CHARACTER SET utf8mb4;

USE ecommerce;

-- 旧结构里的价格带表已废弃
DROP TABLE IF EXISTS dws_price_band;

-- -------------------------------------------------------------
-- 1. ODS：原始明细，字段与 CSV 表头一致
-- -------------------------------------------------------------
DROP TABLE IF EXISTS ods_user_behavior;

CREATE TABLE ods_user_behavior(
  user_id BIGINT,
  item_id BIGINT,
  brand VARCHAR(100),
  brand_id BIGINT,
  item_name VARCHAR(200),
  category VARCHAR(100),
  category_id BIGINT,
  behavior VARCHAR(10),
  ts BIGINT,
  price DECIMAL(10,2),
  dt VARCHAR(30),
  price_level VARCHAR(50)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 1.2 导入：路径改成你的 CSV
LOAD DATA LOCAL INFILE 'D:/data/user_behavior.csv'
INTO TABLE ods_user_behavior
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

-- CSV 里的时间是 2025/1/1 14:33 这种格式，统一成 2025-01-01，避免字符串排序错乱
UPDATE ods_user_behavior
SET dt = DATE_FORMAT(STR_TO_DATE(dt, '%Y/%c/%e %H:%i'), '%Y-%m-%d')
WHERE dt LIKE '%/% %:%';

-- 如果 dt 列是空的时间戳，用下面这句补：
-- UPDATE ods_user_behavior
-- SET dt = FROM_UNIXTIME(ts) WHERE dt IS NULL OR dt = '';


-- -------------------------------------------------------------
-- 2. DWD：维表与事实表
-- -------------------------------------------------------------
DROP TABLE IF EXISTS dim_goods;

CREATE TABLE dim_goods(
  item_id BIGINT PRIMARY KEY,
  item_name VARCHAR(200),
  category VARCHAR(100),
  brand VARCHAR(100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO dim_goods(item_id, item_name, category, brand)
SELECT item_id, MAX(item_name), MAX(category), MAX(brand)
FROM ods_user_behavior
GROUP BY item_id;


DROP TABLE IF EXISTS dim_users;

CREATE TABLE dim_users(
  user_id BIGINT PRIMARY KEY,
  first_dt VARCHAR(30),
  last_dt VARCHAR(30)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO dim_users(user_id, first_dt, last_dt)
SELECT user_id, MIN(dt), MAX(dt)
FROM ods_user_behavior
GROUP BY user_id;


DROP TABLE IF EXISTS fact_behavior;

CREATE TABLE fact_behavior(
  user_id BIGINT,
  item_id BIGINT,
  behavior VARCHAR(10),
  ts BIGINT,
  dt VARCHAR(30),
  price DECIMAL(10,2),
  price_level VARCHAR(50),
  KEY idx_item (item_id),
  KEY idx_user (user_id),
  KEY idx_dt (dt)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO fact_behavior(user_id, item_id, behavior, ts, dt, price, price_level)
SELECT user_id, item_id, behavior, ts, dt, price, price_level
FROM ods_user_behavior;


-- -------------------------------------------------------------
-- 3. DWS 1：商品
-- -------------------------------------------------------------
DROP TABLE IF EXISTS dws_item_hot;

CREATE TABLE dws_item_hot(
  item_id BIGINT PRIMARY KEY,
  item_name VARCHAR(200),
  category VARCHAR(100),
  brand VARCHAR(100),
  pv_count INT,
  fav_count INT,
  cart_count INT,
  buy_count INT,
  buyer_count INT,
  sales_amount DECIMAL(12,2),
  KEY idx_buy (buy_count),
  KEY idx_amount (sales_amount)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO dws_item_hot
SELECT
  g.item_id,
  g.item_name,
  g.category,
  g.brand,
  SUM(IF(f.behavior='pv',1,0)),
  SUM(IF(f.behavior='fav',1,0)),
  SUM(IF(f.behavior='cart',1,0)),
  SUM(IF(f.behavior='buy',1,0)),
  COUNT(DISTINCT IF(f.behavior='buy', f.user_id, NULL)),
  ROUND(SUM(IF(f.behavior='buy', f.price, 0)), 2)
FROM fact_behavior f
JOIN dim_goods g ON f.item_id = g.item_id
GROUP BY g.item_id, g.item_name, g.category, g.brand;


-- -------------------------------------------------------------
-- 4. DWS 2：品牌
-- -------------------------------------------------------------
DROP TABLE IF EXISTS dws_brand_sales;

CREATE TABLE dws_brand_sales(
  brand VARCHAR(100) PRIMARY KEY,
  buy_count INT,
  buyer_count INT,
  sales_amount DECIMAL(12,2),
  avg_amount DECIMAL(12,2),
  KEY idx_amount (sales_amount)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO dws_brand_sales
SELECT
  g.brand,
  SUM(IF(f.behavior='buy',1,0)),
  COUNT(DISTINCT IF(f.behavior='buy', f.user_id, NULL)),
  ROUND(SUM(IF(f.behavior='buy', f.price, 0)), 2),
  ROUND(
    SUM(IF(f.behavior='buy', f.price, 0)) /
    NULLIF(COUNT(DISTINCT IF(f.behavior='buy', f.user_id, NULL)), 0)
  , 2)
FROM fact_behavior f
JOIN dim_goods g ON f.item_id = g.item_id
WHERE g.brand IS NOT NULL AND g.brand <> ''
GROUP BY g.brand;


-- -------------------------------------------------------------
-- 5. DWS 3：品类
-- -------------------------------------------------------------
DROP TABLE IF EXISTS dws_category_sales;

CREATE TABLE dws_category_sales(
  category VARCHAR(100) PRIMARY KEY,
  buy_count INT,
  item_count INT,
  buyer_count INT,
  sales_amount DECIMAL(12,2),
  avg_amount DECIMAL(12,2),
  KEY idx_amount (sales_amount)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO dws_category_sales
SELECT
  g.category,
  SUM(IF(f.behavior='buy',1,0)),
  COUNT(DISTINCT g.item_id),
  COUNT(DISTINCT IF(f.behavior='buy', f.user_id, NULL)),
  ROUND(SUM(IF(f.behavior='buy', f.price, 0)), 2),
  ROUND(
    SUM(IF(f.behavior='buy', f.price, 0)) /
    NULLIF(COUNT(DISTINCT IF(f.behavior='buy', f.user_id, NULL)), 0)
  , 2)
FROM fact_behavior f
JOIN dim_goods g ON f.item_id = g.item_id
WHERE g.category IS NOT NULL AND g.category <> ''
GROUP BY g.category;


-- -------------------------------------------------------------
-- 6. DWS 4：每日趋势
-- -------------------------------------------------------------
DROP TABLE IF EXISTS dws_daily_trend;

CREATE TABLE dws_daily_trend(
  dt VARCHAR(10) PRIMARY KEY,
  pv_count INT,
  cart_count INT,
  buy_count INT,
  buyer_count INT,
  sales_amount DECIMAL(12,2)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO dws_daily_trend
SELECT
  SUBSTR(dt, 1, 10),
  SUM(IF(behavior='pv',1,0)),
  SUM(IF(behavior='cart',1,0)),
  SUM(IF(behavior='buy',1,0)),
  COUNT(DISTINCT IF(behavior='buy', user_id, NULL)),
  ROUND(SUM(IF(behavior='buy', price, 0)), 2)
FROM fact_behavior
GROUP BY SUBSTR(dt, 1, 10);


-- -------------------------------------------------------------
-- 7. DWS 5：用户价值
-- -------------------------------------------------------------
DROP TABLE IF EXISTS dws_user_value;

CREATE TABLE dws_user_value(
  user_id BIGINT PRIMARY KEY,
  pv_count INT,
  fav_count INT,
  cart_count INT,
  buy_count INT,
  total_amount DECIMAL(12,2),
  first_dt VARCHAR(30),
  last_dt VARCHAR(30),
  value_level VARCHAR(20),
  KEY idx_amount (total_amount)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO dws_user_value
SELECT
  user_id,
  SUM(IF(behavior='pv',1,0)),
  SUM(IF(behavior='fav',1,0)),
  SUM(IF(behavior='cart',1,0)),
  SUM(IF(behavior='buy',1,0)),
  ROUND(SUM(IF(behavior='buy', price, 0)), 2),
  MIN(dt),
  MAX(dt),
  CASE
    WHEN SUM(IF(behavior='buy',1,0)) >= 3 THEN '高价值'
    WHEN SUM(IF(behavior='buy',1,0)) = 2 THEN '中价值'
    WHEN SUM(IF(behavior='buy',1,0)) = 1 THEN '一次购买'
    ELSE '仅浏览'
  END
FROM fact_behavior
GROUP BY user_id;


-- -------------------------------------------------------------
-- 8. 自检
-- -------------------------------------------------------------
SELECT 'ods' AS t, COUNT(*) AS n FROM ods_user_behavior
UNION ALL SELECT 'fact', COUNT(*) FROM fact_behavior
UNION ALL SELECT 'item', COUNT(*) FROM dws_item_hot
UNION ALL SELECT 'brand', COUNT(*) FROM dws_brand_sales
UNION ALL SELECT 'category', COUNT(*) FROM dws_category_sales
UNION ALL SELECT 'daily', COUNT(*) FROM dws_daily_trend
UNION ALL SELECT 'user', COUNT(*) FROM dws_user_value;
