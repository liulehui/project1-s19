//Count of Masters champions by player's ID
SELECT DISTINCT COUNT(tournament_id) as count
FROM 
tournament INNER JOIN players ON tournament.single_winner_id = players.id WHERE tournament.series_id = 2;
