with tmp as (
select date, pid, score,rank() over (partition by date order by score desc) as rank from history_score)

select distinct p.id, p.first_name||' '||p.last_name as name from players as p
join tmp on tmp.pid = p.id
where rank < 10