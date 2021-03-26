select
    t2.nameFirst || ' ' || t2.nameLast as name,
    playerID,
    teamID,
    salary
from 
    Salaries t1  # Salaries includes all the salary info for all players
join 
    People t2 on t2.playerID = t1.playerID  # People table includes all the name info for all players
order by salary desc
limit 20;

-- join and group by
-- top paid player for each team in 2016
select
    t1.yearID,
    t1.teamID,
    t2.nameFirst || ' ' || t2.nameLast as name,
    max(salary)
from 
    Salaries t1
join 
    People t2 on t1.playerID = t2.playerID
where
    t1.yearID = '2016'
group by
    t1.teamID