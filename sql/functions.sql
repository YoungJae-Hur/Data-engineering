-- functions, SUBSTR -> brings the substr of name column from 1-4 elements
select SUBSTR(name, 1, 7) from mytable;

-- UPPER, changes all alphabets into uppercase
select UPPER(name) from mytable;

-- LENGTH, gets the number of alphabets in name column 
select LENGTH(name) from mytable;

-- DATE, DATETIME
select DATE('NOW');
select DATE(current_timestamp);

select DATETIME(current_timestamp, '+1 DAY'); -- adds another day from current datetime

select DATETIME('NOW');
select current_timestamp;