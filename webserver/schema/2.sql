//Show one player's history score by time:
SELECT 
date,score
FROM players 
INNER JOIN history_score ON players.id = history_score.pid WHERE history_score.pid = 
'n409'
ORDER BY date DESC LIMIT 20;
