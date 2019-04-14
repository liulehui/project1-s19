//Show lost single match statistics from players:
SELECT 
loser_aces, loser_double_faults, loser_first_serves_in, loser_first_serves_total, loser_first_serve_return_won, loser_first_serve_return_total, loser_second_serve_return_won, loser_second_serve_return_total	loser_break_points_converted, loser_break_points_return_total,	loser_service_games_played,	loser_return_games_played,	loser_return_points_won,	loser_return_points_total,	loser_total_points_won,	loser_total_points_total
FROM 
(single_match 
	INNER JOIN players ON single_match.losers_id = players.id)
	INNER JOIN match ON matches.match_id = single_match.mid
WHERE players.id = "n409" LIMIT 10;
