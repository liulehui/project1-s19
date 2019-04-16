
with tmp as
(select pid,max(date) from history_score group by pid),

tmp1 as (
select tmp.pid,first_name||' '||last_name as name ,tmp.max,score,rank() over (order by score DESC) from history_score, tmp, players
where history_score.pid = tmp.pid
and tmp.pid = players.id
and history_score.date = tmp.max)

select name, rank from tmp1 where pid = 'f324';
