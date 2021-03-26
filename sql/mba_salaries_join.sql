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