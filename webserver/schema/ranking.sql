with tmp as
(select pid,max(date) from history_score group by pid)
select tmp.pid,tmp.max,score,rank() over (order by score DESC) from history_score, tmp
where history_score.pid = tmp.pid
and history_score.date = tmp.max;
