-- =============================================================
-- 电商用户行为数仓：ODS → DWD → DWS
-- 字段与 CSV 表头一致，timestamp 改名为 ts，datetime 改名为 dt
-- =============================================================

CREATE DATABASE IF NOT EXISTS ecommerce;
USE ecommerce;

-- -------------------------------------------------------------
-- ODS：原始明细
-- -------------------------------------------------------------
DROP TABLE IF EXISTS ods_user_behavior;

CREATE TABLE ods_user_behavior(
  user_id BIGINT,
  item_id BIGINT,
  brand STRING,
  brand_id BIGINT,
  item_name STRING,
  category STRING,
  category_id BIGINT,
  behavior STRING,
  ts BIGINT,
  price DECIMAL(10,2),
  dt STRING,
  price_level STRING
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE
TBLPROPERTIES ('skip.header.line.count'='1');

-- 装载：改成你机器上的实际路径
LOAD DATA LOCAL INPATH '/data/user_behavior.csv'
OVERWRITE INTO TABLE ods_user_behavior;


-- -------------------------------------------------------------
-- DWD：维表 + 事实表
-- -------------------------------------------------------------
DROP TABLE IF EXISTS dim_goods;

CREATE TABLE dim_goods(
  item_id BIGINT,
  item_name STRING,
  category STRING,
  brand STRING
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE;

INSERT OVERWRITE TABLE dim_goods
SELECT
  item_id,
  MAX(item_name),
  MAX(category),
  MAX(brand)
FROM ods_user_behavior
GROUP BY item_id;


DROP TABLE IF EXISTS dim_users;

CREATE TABLE dim_users(
  user_id BIGINT,
  first_dt STRING,
  last_dt STRING
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE;

INSERT OVERWRITE TABLE dim_users
SELECT user_id, MIN(dt), MAX(dt)
FROM ods_user_behavior
GROUP BY user_id;


DROP TABLE IF EXISTS fact_behavior;

CREATE TABLE fact_behavior(
  user_id BIGINT,
  item_id BIGINT,
  behavior STRING,
  ts BIGINT,
  dt STRING,
  price DECIMAL(10,2),
  price_level STRING
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE;

INSERT OVERWRITE TABLE fact_behavior
SELECT user_id, item_id, behavior, ts, dt, price, price_level
FROM ods_user_behavior;


-- -------------------------------------------------------------
-- DWS 1：商品维度（销量、销售额、转化）
-- -------------------------------------------------------------
DROP TABLE IF EXISTS dws_item_hot;

CREATE TABLE dws_item_hot(
  item_id BIGINT,
  item_name STRING,
  category STRING,
  brand STRING,
  pv_count INT,
  fav_count INT,
  cart_count INT,
  buy_count INT,
  buyer_count INT,
  sales_amount DECIMAL(12,2)
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE;

INSERT OVERWRITE TABLE dws_item_hot
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
-- DWS 2：品牌维度
-- -------------------------------------------------------------
DROP TABLE IF EXISTS dws_brand_sales;

CREATE TABLE dws_brand_sales(
  brand STRING,
  buy_count INT,
  buyer_count INT,
  sales_amount DECIMAL(12,2),
  avg_amount DECIMAL(12,2)
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE;

INSERT OVERWRITE TABLE dws_brand_sales
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
-- DWS 3：品类维度
-- -------------------------------------------------------------
DROP TABLE IF EXISTS dws_category_sales;

CREATE TABLE dws_category_sales(
  category STRING,
  buy_count INT,
  item_count INT,
  buyer_count INT,
  sales_amount DECIMAL(12,2),
  avg_amount DECIMAL(12,2)
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE;

INSERT OVERWRITE TABLE dws_category_sales
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
-- DWS 4：价格带
-- -------------------------------------------------------------
DROP TABLE IF EXISTS dws_price_band;

CREATE TABLE dws_price_band(
  price_level STRING,
  item_count INT,
  pv_count INT,
  buy_count INT,
  buyer_count INT,
  sales_amount DECIMAL(12,2),
  convert_rate DECIMAL(8,4)
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE;

INSERT OVERWRITE TABLE dws_price_band
SELECT
  price_level,
  COUNT(DISTINCT item_id),
  SUM(IF(behavior='pv',1,0)),
  SUM(IF(behavior='buy',1,0)),
  COUNT(DISTINCT IF(behavior='buy', user_id, NULL)),
  ROUND(SUM(IF(behavior='buy', price, 0)), 2),
  ROUND(
    SUM(IF(behavior='buy',1,0)) / NULLIF(SUM(IF(behavior='pv',1,0)), 0)
  , 4)
FROM fact_behavior
WHERE price_level IS NOT NULL AND price_level <> ''
GROUP BY price_level;


-- -------------------------------------------------------------
-- DWS 5：每日趋势
-- -------------------------------------------------------------
DROP TABLE IF EXISTS dws_daily_trend;

CREATE TABLE dws_daily_trend(
  dt STRING,
  pv_count INT,
  cart_count INT,
  buy_count INT,
  buyer_count INT,
  sales_amount DECIMAL(12,2)
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE;

INSERT OVERWRITE TABLE dws_daily_trend
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
-- DWS 6：用户价值
-- -------------------------------------------------------------
DROP TABLE IF EXISTS dws_user_value;

CREATE TABLE dws_user_value(
  user_id BIGINT,
  pv_count INT,
  fav_count INT,
  cart_count INT,
  buy_count INT,
  total_amount DECIMAL(12,2),
  first_dt STRING,
  last_dt STRING,
  value_level STRING
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE;

INSERT OVERWRITE TABLE dws_user_value
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
