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
    UserName varchar(69),
    FOREIGN KEY (UserName) REFERENCES USERNAME (UserName),
    Event varChar(420),
    StartTime varchar(69),
    EndTime varchar(69),
    StartDate(69)
);


SHOW TABLES;
