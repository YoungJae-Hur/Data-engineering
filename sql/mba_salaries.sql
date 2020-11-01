-- 1. Top Ten Salaries: select, where, order by
--SELECT * FROM Salaries LIMIT 10;

-- SELECT yearID FROM Salaries LIMIT 10;

--SELECT 
--    yearID, playerID, salary 
--FROM Salaries LIMIT 10;

-- SELECT * FROM 
-- Salaries 
-- WHERE teamID="LAN" 
-- and yearID="2016" 
-- ORDER BY salary  
-- DESC limit 100; -- DESC, ASC for ordering

-- 2. SUM, AVG
-- select * from Salaries
-- where playerID = 'rodrial01'
-- order by yearID asc; 

-- 2.1 find the summation of aggregate of salaries in entire career
-- select sum(salary)
-- from Salaries   
-- where playerID = 'rodrial01';

-- 3. concat function, DISTINCT
-- select nameFirst || ' ' || nameLast -- MySQL version select CONCAT(nameFirst, nameLast) from People limit 10;
-- as Fullname
-- from People
-- limit 15; 

-- 3.1 find full name by its playerID
select nameFirst || ' ' || nameLast
as Fullname
from People
where playerID = 'rodrial01'; -- ryuhy01

-- SELECT * FROM -- selecting top 10 salaries from NL MLB players in LA Dodgers
-- 	Salaries
-- WHERE yearID = '2016'  
-- AND lgID = 'NL'
-- AND teamID = 'LAN'
-- ORDER BY salary 
-- DESC LIMIT 10;

-- SELECT * FROM Salaries where playerID='kershcl01' ORDER by yearID DESC limit 10; -- Kershaw's Salaries in decade

-- sum of Kershaw's Salaries from LAD, wow Kershaw is rich bro...
-- SELECT sum(salary) -- also can use AVG, etc for other functions
-- FROM Salaries
-- WHERE playerID='kershcl01';

 -- Ryu's Salaries in 3 years
-- SELECT * FROM Salaries where playerID='ryuhy01' ORDER by yearID DESC limit 10;

-- get names of players from People table
-- SELECT nameFirst || ' ' || nameLast AS name from People limit 10;

-- Find out name of player by playerID
-- SELECT nameFirst || ' ' || nameLast FROM People WHERE  playerID='ryuhy01' ;

-- Find out the unique number of names in Players
-- SELECT COUNT(DISTINCT(nameFirst || ' ' || nameLast)) FROM People;

-- find out duplicate names
-- SELECT nameFirst || ' ' || nameLast AS name, COUNT(*) from People GROUP BY name HAVING COUNT(*) > 1

-- Figure out the most highest salaries in MLB team
--SELECT
--	yearID,
--	teamID,
--	SUM(salary) AS total_salary
--FROM
--	Salaries
--GROUP BY yearID, teamID
--ORDER BY SUM(salary) DESC
