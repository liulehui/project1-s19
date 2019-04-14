select tournament_id,name,start_year as year,location,surface,condition,singer_winner_id
from tournament
where tournament_id = 580
order by start_year desc
limit 10;