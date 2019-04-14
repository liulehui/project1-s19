//Show won single match statistics (all) from players:
SELECT 
winner_aces, winner_double_faults, winner_first_serves_in, winner_first_serves_total, winner_first_serve_points_won, winner_first_serve_points_total, winner_second_serve_points_won, winner_second_serve_points_total, winner_break_points_saved, winner_break_points_serve_total, winner_service_points_won, winner_service_points_total, winner_first_serve_return_won, winner_first_serve_return_total, winner_second_serve_return_won, winner_second_serve_return_total, winner_break_points_converted, winner_break_points_return_total, winner_service_games_played, winner_return_games_played, winner_return_points_won, winner_return_points_total, winner_total_points_won, winner_total_points_total 
FROM 
(single_match 
	INNER JOIN players ON single_match.winner_id = players.id)
	INNER JOIN matches ON matches.match_id = single_matches.mid
WHERE players.id = "n409" LIMIT 10;
