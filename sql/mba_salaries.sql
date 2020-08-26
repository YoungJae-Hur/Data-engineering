-- SELECT * FROM Salaries LIMIT 100;

-- SELECT yearID FROM Salaries LIMIT 10;

-- SELECT 
-- 	yearID, playerID, salary 
-- FROM Salaries LIMIT 10;

-- SELECT * FROM Salaries ORDER BY salary DESC limit 100; -- DESC, ASC for ordering

SELECT * FROM
	Salaries
WHERE yearID = '2016'  
AND lgID = 'NL'
AND teamID = 'LAN'
ORDER BY salary 
DESC LIMIT 10;
