
with tmp as
(select pid,max(date) from history_score where date<'2017-04-11' group by pid)
select first_name||' '||last_name as name ,tmp.max,score,rank() over (order by score DESC) from history_score, tmp, players
where history_score.pid = tmp.pid
and tmp.pid = players.id
and history_score.date = tmp.max
limit 10;
