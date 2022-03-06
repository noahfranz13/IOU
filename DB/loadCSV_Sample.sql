LOAD DATA INFILE "/var/lib/mysql-files/EVENT_TABLE.csv"
INTO TABLE EVENT_TABLE
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

/*You can replace “*” with the join expression for your query.*/
