-- 建立存放 SCUT-FBP5500_v2 原始資料的表，只關注 rater、filename、rating 三個欄位
CREATE TABLE `all_ratings` (
  `rater` varchar(2),
  `filename` varchar(15),
  `rating` varchar(1)
);

-- 將資料從 csv 匯入 mysql 的參考指令
LOAD DATA INFILE '/path/to/my_file.csv'
INTO TABLE my_table
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- 每張照片的平均分數的表
CREATE TABLE `avg_rating` (
  `filename` varchar(15),
  `avg_rating` float 
);

-- 用 DB 算出每張照片的平均分數，存起來供訓練模型用
INSERT INTO `avg_rating` (`filename`, `avg_rating`)
SELECT a.filename, ROUND(AVG(a.rating), 2)
FROM `all_ratings` as a
GROUP BY a.filename;

-- 存放我的測試照片的表格
CREATE TABLE my_face_rating(
	`smile` VARCHAR(5),
    `hair_style` VARCHAR(5),
    `beard` VARCHAR(5),
    `glasses` VARCHAR(5),
    `filename` VARCHAR(25) PRIMARY KEY,
    `picture_done` VARCHAR(1),
    `rating` FLOAT
);
