//Count of GS champions by player's ID
SELECT DISTINCT COUNT(tournament_id)
FROM 
tournament INNER JOIN players ON tournament.single_winner_id = players.id WHERE tournament.series_id = 1;
