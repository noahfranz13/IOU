SELECT *
INTO OUTFILE ‘/home/ubuntu/Documents/IOU/EVENT_TABLE.csv’
FIELDS TERMINATED BY ‘,’
ENCLOSED BY ‘”‘
ESCAPED BY ‘\\’
LINES TERMINATED BY ‘\n’
FROM EVENT_TABLE

/*You can replace “*” with the join expression for your query.*/
