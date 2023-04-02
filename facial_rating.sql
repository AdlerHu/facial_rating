CREATE TABLE my_face_rating(
	`No` INT PRIMARY KEY AUTO_INCREMENT,
	`smile` VARCHAR(5),
    `hair_style` VARCHAR(5),
    `beard` VARCHAR(5),
    `glasses` VARCHAR(5),
    `filename` VARCHAR(25),
    `rating` FLOAT
);

INSERT INTO `my_face_rating` (`smile`, `hair_style`, `beard`, `glasses`, `filename`, `picture_done`, `rating`) 
VALUES ('不開心', '殺手', '小山羊鬍', '窄邊橢圓', '不開心_殺手_小山羊鬍_窄邊橢圓.jpg', '0', 2.5);

UPDATE `my_face_rating` SET `rating` = 3.5 WHERE `filename` = '原始_原始_原始_原始.jpg';


LOAD DATA INFILE '/var/lib/mysql-files/All_Ratings.csv' INTO TABLE all_face_ratings FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 0 ROWS;

SELECT filename, ROUND(AVG(rating), 3)
FROM `all_face_ratings` 
GROUP BY filename;


CREATE TABLE avg_rating (
  filename VARCHAR(12),  
  avg_rating FLOAT
);

CREATE TABLE all_face_rating (
  filename VARCHAR(12),  
  rating INT
);

INSERT INTO avg_rating (filename, avg_rating)
SELECT filename, ROUND(AVG(rating), 3)
FROM `all_face_ratings` 
GROUP BY filename;