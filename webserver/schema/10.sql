//Surface and duration for histogram given tournament ID
SELECT distinct name, surface
FROM 
tournament INNER JOIN matches ON tournament.tournament_id = matches.t_id WHERE tournament.tournament_id = 540;
