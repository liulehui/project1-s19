//Count of GS champions by player's ID
with tmp as (
select pid, rank() over (order by score DESC) as rank from history_score)

select players.id, first_name||' '||last_name as name, rank from players join tmp on tmp.pid = players.id;
