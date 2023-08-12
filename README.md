#   Membership create
A membership system with  MySQL version 
Chinese Only 
Help people to save their member's data 
The MySQL table you need to insert into your database
CREATE TABLE
    `membership_list` (
        `Member_ID` int NOT NULL AUTO_INCREMENT,
        `M_NAME` varchar(10) NOT NULL,
        `M_Phone` varchar(20) NOT NULL,
        `M_Adress` varchar(100) DEFAULT NULL,
        `M_Gender` varchar(10) DEFAULT NULL,
        `M_Birth` date DEFAULT NULL,
        PRIMARY KEY (`Member_ID`)
    ) ENGINE = InnoDB AUTO_INCREMENT = 4 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci

  Also, you have to change the data in lines 86~92 with your database detail 
  Enjoy it
