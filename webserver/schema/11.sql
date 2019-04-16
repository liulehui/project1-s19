//Past champions and how many times given tournament ID
SELECT first_name||' '||last_name as name, COUNT (start_year) as count
FROM 
tournament INNER JOIN players ON tournament.singer_winner_id = players.id
WHERE tournament.tournament_id = 540
group by first_name,last_name
order by count desc;
