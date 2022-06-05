CREATE DataBase if not exists emp ;
USE EMP;
Create TABLE if not exists User(`User ID` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
			`User name` varchar(255),
            `User DOB` date,
            `User email` varchar(255),
            `User Created Date` date);

CREATE TABLE if not exists Bank_Account (
						`bank account id` int NOT NULL AUTO_INCREMENT primary KEY,
                        `bank account number` int NOT NULL AUTO_INCREMENT,
                        `is user active` bool,
                        `amount` int,
                        `User Id` int , 
                        CONSTRAINT fk_category FOREIGN KEY (`User Id`) REFERENCES `User`(`User Id`)
                     );
CREATE TABLE IF NOT EXISTS `Transaction Table`(
						`Transcation Date` DATE,
                        `bank account id` INT,
                        `User Id` INT,
                        `withdrawn amount` FLOAT,
                        CONSTRAINT fk_category_1 
                        FOREIGN KEY (`User Id`) REFERENCES `User`(`User Id`), 
                        FOREIGN KEY (`bank account id`) REFERENCES Bank_Account(`bank account id`)                       
);                     
show tables ;   

drop trigger IF EXISTS update_amount;
delimiter //
CREATE TRIGGER `update_amount` BEFORE INSERT ON `transaction table` FOR EACH ROW BEGIN
	UPDATE emp.bank_account SET `amount`= `amount`-NEW.`withdrawn amount`
    WHERE `user id`=NEW.`User Id`;
end//
delimiter ;

use emp;
delimiter //
CREATE PROCEDURE spCheck_amount( IN
user_name varchar(250),
user_id int)
BEGIN
	SELECT user.`user name`,bank_account.amount FROM bank_account
    JOIN user on bank_account.`user id`=user.`user id`
    WHERE user.`User name`=user_name and user.`user id`=user_id;
end//
delimiter ;

CALL spCheck_amount('sarad',1);    

use emp;
DROP procedure IF EXISTS spWithdraw_ammount;

delimiter //
CREATE PROCEDURE spWithdraw_ammount(IN
user_id varchar(250),
bank_account_id int,
amount_1 int
)             
BEGIN
	IF (((select emp.bank_account.`amount` from bank_account where user_id=`user id`)-amount_1)>5000)
		THEN
			INSERT INTO emp.`transaction table` (`Transcation Date`,`user id`,`bank account id`,`withdrawn amount`)
			VALUES (now(),user_id,bank_account_id,amount_1);
    ELSE
		SELECT 'Amout is insufficient' AS MSG;
	END IF;
END//
delimiter ;
CALL spWithdraw_ammount(2,2,3);


use emp;
DROP PROCEDURE IF EXISTS spTransactionCheck;
delimiter //
CREATE PROCEDURE spTransactionCheck(IN user_id int, IN strtdate char(50),
									IN enddate char(50)
									)
BEGIN
	SELECT `user id`,`Transcation Date`,`withdrawn amount` FROM emp.`transaction table` where
    (`user id`=user_id) and (`transaction table`.`Transcation Date` between cast(strtdate as DATE) and cast(enddate as DATE));
END//
delimiter ;

CALL spTransactionCheck(1,'2022-06-02','2022-06-06');