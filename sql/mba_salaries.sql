-- SELECT * FROM Salaries LIMIT 100;

-- SELECT yearID FROM Salaries LIMIT 10;

-- SELECT 
-- 	yearID, playerID, salary 
-- FROM Salaries LIMIT 10;

-- SELECT * FROM Salaries ORDER BY salary DESC limit 100; -- DESC, ASC for ordering

-- SELECT * FROM -- selecting top 10 salaries from NL MLB players in LA Dodgers
-- 	Salaries
-- WHERE yearID = '2016'  
-- AND lgID = 'NL'
-- AND teamID = 'LAN'
-- ORDER BY salary 
-- DESC LIMIT 10;

-- SELECT * FROM Salaries where playerID='kershcl01' ORDER by yearID DESC limit 10 -- Kershaw's Salaries in decade

-- sum of Kershaw's Salaries from LAD, wow Kershaw is rich bro...
SELECT sum(salary)
FROM Salaries
WHERE playerID='kershcl01'


-- SELECT * FROM Salaries where playerID='ryuhy01' ORDER by yearID DESC limit 10 -- Ryu's Salaries in 3 years
