select p.last_name,p.first_name,p.birthday,p.height,p.weight,p.nationality,p.start_pro,
m.year,m.duration,m.level,m.winner_sets_won,m.loser_sets_won,t.name,lp.last_name ||' '||lp.first_name as loser_name
from players as p
join single_match as s on p.id = s.winner_id
join matches as m on m.match_id = s.mid
join players as lp on lp.id = s.losers_id
join tournament as t on m.t_id = t.tournament_id
where p.id = 'f324'
order by m.year DESC
limit 1;