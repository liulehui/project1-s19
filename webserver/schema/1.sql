//Show Top 10 ranking players
with tmp as (
SELECT
first_name||' '||last_name, score
FROM players INNER JOIN history_score ON players.id = history_score.pid
WHERE history_score.date = (SELECT date from history_score where date < '2016-11-11' order by date DESC limit 1)
ORDER BY score DESC LIMIT 10;)
select