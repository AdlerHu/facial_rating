CREATE TABLE my_face_rating(
	`No` INT PRIMARY KEY AUTO_INCREMENT,
	`smile` VARCHAR(5),
    `hair_style` VARCHAR(5),
    `beard` VARCHAR(5),
    `glasses` VARCHAR(5),
    `filename` VARCHAR(25),
    `picture_done` VARCHAR(1),
    `rating` FLOAT
);

INSERT INTO `my_face_rating` (`smile`, `hair_style`, `beard`, `glasses`, `filename`, `picture_done`, `rating`) 
VALUES ('不開心', '殺手', '小山羊鬍', '窄邊橢圓', '不開心_殺手_小山羊鬍_窄邊橢圓.jpg', '0', 2.5);

UPDATE `my_face_rating` SET `rating` = 3.5 WHERE `filename` = '原始_原始_原始_原始.jpg';