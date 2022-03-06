SELECT *
INTO OUTFILE ‘/tmp/patients.csv’
FIELDS TERMINATED BY ‘,’
ENCLOSED BY ‘”‘
ESCAPED BY ‘\\’
LINES TERMINATED BY ‘\n’
FROM patients

/*You can replace “*” with the join expression for your query.*/
