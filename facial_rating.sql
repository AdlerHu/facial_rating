CREATE TABLE all_face_ratings (
  filename VARCHAR(12),  
  rating INT
);

CREATE TABLE avg_rating (
  filename VARCHAR(12),  
  avg_rating FLOAT
);

LOAD DATA INFILE '/var/lib/mysql-files/All_Ratings.csv' INTO TABLE all_face_ratings FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 0 ROWS;

INSERT INTO avg_rating (filename, avg_rating)
SELECT filename, ROUND(AVG(rating), 3)
FROM `all_face_ratings` 
GROUP BY filename;

CREATE TABLE my_face_rating(
	`No` INT PRIMARY KEY AUTO_INCREMENT,
	`smile` VARCHAR(5),
    `hair_style` VARCHAR(5),
    `beard` VARCHAR(5),
    `glasses` VARCHAR(5),
    `filename` VARCHAR(25),
    `rating` FLOAT
);
