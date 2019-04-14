//Show average aces in won games from players:
SELECT AVG(winner_aces) 
FROM 
single_match 
	INNER JOIN players ON single_match.winner_id = players.id
	INNER JOIN matches ON matches.match_id = single_matches.mid
GROUP BY players.id;
