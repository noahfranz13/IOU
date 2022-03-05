/*DROP DATABASE IOU_DB;
CREATE DATABASE IOU_DB;*/
USE IOU_DB;

CREATE TABLE USERNAME(
    UserName varChar(69) PRIMARY KEY,
    FirstName varchar(69),
    LastName varchar(69),
    Email varchar(420),
    Password varchar(69)
);

CREATE TABLE EVENT_TABLE (
    UserName varChar(69),
    FOREIGN KEY (UserName) REFERENCES USERNAME (UserName)
);


SHOW TABLES;
