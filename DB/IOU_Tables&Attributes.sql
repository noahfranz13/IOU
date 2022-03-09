/*DROP DATABASE IOU_DB;
CREATE DATABASE IOU_DB;*/
USE IOU_DB;

CREATE TABLE USERNAME(
    UserName varChar(25) PRIMARY KEY,
    FirstName varchar(15),
    LastName varchar(20),
    Email varchar(320),
    Password varchar(30)
);

CREATE TABLE EVENT_TABLE (
    UserName varchar(25),
    FOREIGN KEY (UserName) REFERENCES USERNAME (UserName),
    Event varChar(350),
    StartTime varchar(15),
    EndTime varchar(15),
    StartDate varchar(15)
);

CREATE TABLE OWE_TABLE (
    ower varchar(25),
    owes varchar(25),
    amount float
);

CREATE TABLE REQUESTS (
    Requestor varchar(25),
    StartDate varchar(15),
    StartTime varchar(15),
    EndTime varchar(15),
    EventName varchar(30)
);


SHOW TABLES;
