#!/usr/bin/env python2.7

"""
Columbia W4111 Intro to databases
Example webserver

To run locally

    python server.py

Go to http://localhost:8111 in your browser


A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
import json
from datetime import datetime
import os
import time
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response
import pandas as pd

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

# XXX: The Database URI should be in the format of:
#
#     postgresql://USER:PASSWORD@<IP_OF_POSTGRE_SQL_SERVER>/<DB_NAME>
#
# For example, if you had username ewu2493, password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://ewu2493:foobar@<IP_OF_POSTGRE_SQL_SERVER>/postgres"
#
# For your convenience, we already set it to the class database

# Use the DB credentials you received by e-mail
DB_USER = "ll3238"
DB_PASSWORD = "pcuuGKCTf1"

DB_SERVER = "w4111.cisxo09blonu.us-east-1.rds.amazonaws.com"

DATABASEURI = "postgresql://" + DB_USER + ":" + DB_PASSWORD + "@" + DB_SERVER + "/w4111"

#
# This line creates a database engine that knows how to connect to the URI above
#
engine = create_engine(DATABASEURI)

# Here we create a test table and insert some values in it
engine.execute("""DROP TABLE IF EXISTS test;""")
engine.execute("""CREATE TABLE IF NOT EXISTS test (
  id serial,
  name text
);""")
engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


@app.before_request
def before_request():
    """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request

  The variable g is globally accessible
  """
    try:
        g.conn = engine.connect()
    except:
        print("uh oh, problem connecting to database")
        import traceback;
        traceback.print_exc()
        g.conn = None


@app.teardown_request
def teardown_request(exception):
    """
  At the end of the web request, this makes sure to close the database connection.
  If you don't the database could run out of memory!
  """
    try:
        g.conn.close()
    except Exception as e:
        pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to e.g., localhost:8111/foobar/ with POST or GET then you could use
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
    print(request.args)
    query = 'select distinct name, tournament_id as tid from tournament where series_id  = 1'
    cursor = g.conn.execute(query)
    gss = []
    for result in cursor:
        gs = {'name': result['name'], 'tid': result['tid']}
        gss.append(gs)
    cursor.close()

    query = 'select distinct name, tournament_id as tid from tournament where series_id = 2 and start_year = 2016'
    cursor = g.conn.execute(query)
    atp_masters = []
    for result in cursor:
        atp_master = {'name': result['name'], 'tid': result['tid']}
        atp_masters.append(atp_master)

    cursor.close()

    # print(gss)
    # print(atp_masters)

    query = """with tmp as (
    select date, pid, score,rank() over (partition by date order by score desc) as rank from history_score)

    select distinct p.id, p.first_name||' '||p.last_name as name from players as p
    join tmp on tmp.pid = p.id
    where rank < 10"""
    cursor = g.conn.execute(query)
    top10_players = []
    for result in cursor:
        # print(result)
        top10_players.append(result)
    cursor.close()

    return render_template("introduction.html", gss=gss, atp_masters=atp_masters, players=top10_players,
                           title='Landing Page')
@app.route("/queryplayer", methods=['POST'])
def queryplayers():
    print(request.form)
    name = request.form['name']
    print(name)
    print(type(name))
    name = name.lower()


    sql_query = """select id, first_name||' '||last_name as name from players 
    where LOWER(first_name) like '%%{}%%' or LOWER(last_name) like '%%{}%%';""".format(name,name)

    print(sql_query)

    cursor = g.conn.execute(sql_query)
    similar_players = []
    for result in cursor:
        print(result)
        similar_player = {'pid': result['id'], 'name': result['name']}
        similar_players.append(similar_player)
    cursor.close()
    return render_template(
        'queryplayer.html',
        title="ranking",
        players=similar_players)
#
# @app.route('/another')
# def another():
#     return render_template("anotherfile.html")


# Example of adding new data to the database
# @app.route('/add', methods=['POST'])
# def add():
#     name = request.form['name']
#     print(name)
#     cmd = 'INSERT INTO test(name) VALUES (:name1), (:name2)';
#     g.conn.execute(text(cmd), name1=name, name2=name);
#     return redirect('/')


#
# @app.route('/login')
# def login():
#     abort(401)
#     this_is_never_executed()


@app.route("/tournaments")
def tournaments():
    # select all the grand slams
    query = 'select distinct name, tournament_id as tid from tournament where series_id  = 1'
    cursor = g.conn.execute(query)
    gss = []
    for result in cursor:
        gs = {'name': result['name'], 'tid': result['tid']}
        gss.append(gs)
    cursor.close()

    query = 'select distinct name, tournament_id as tid from tournament where series_id = 2 and start_year = 2016'
    cursor = g.conn.execute(query)
    atp_masters = []
    for result in cursor:
        atp_master = {'name': result['name'], 'tid': result['tid']}
        atp_masters.append(atp_master)

    cursor.close()
    print(gss)
    print(atp_masters)
    return render_template(
        'tournaments.html',
        title="tournaments",
        gss=gss, atp_masters=atp_masters)


@app.route("/tournaments/<int:tid>")
def tournament(tid):
    tid = tid
    cmd = """
    SELECT distinct name, surface FROM tournament INNER JOIN matches ON tournament.tournament_id = matches.t_id 
    WHERE tournament.tournament_id = {} and start_year = 2016""".format(tid)
    cursor = g.conn.execute(cmd)
    result = cursor.first()
    name = result['name']
    surface = result['surface']
    cursor.close()

    # past champions
    past_champions = []
    cmd = """SELECT players.id,first_name||' '||last_name as name, COUNT (start_year) as count
FROM 
tournament INNER JOIN players ON tournament.singer_winner_id = players.id
WHERE tournament.tournament_id = {}
group by players.id,first_name,last_name
order by count desc;""".format(tid)

    cursor = g.conn.execute(cmd)
    for result in cursor:
        past_champion = {'pid': result['id'],'name': result['name'], 'count': result['count']}
        past_champions.append(past_champion)
    cursor.close()
    print(past_champions)
    return render_template('tournament.html', title=tid, name = name, surface = surface, past_champions = past_champions)


@app.route("/players")
def players():
    query = """with tmp as (
select date, pid, score,rank() over (partition by date order by score desc) as rank from history_score)

select distinct p.id, p.first_name||' '||p.last_name as name from players as p
join tmp on tmp.pid = p.id
where rank < 10"""
    cursor = g.conn.execute(query)
    top10_players = []
    for result in cursor:
        print(result)
        top10_players.append(result)
    cursor.close()
    return render_template('players.html', title='players',
                           players=top10_players)


@app.route("/players/<string:pid>")
def player(pid):
    pid = "\'" + pid + "\'"
    print(pid)

    cursor = g.conn.execute("""
    select p.last_name,p.first_name,p.birthday,p.height,p.weight,p.nationality,p.start_pro,
m.year,m.duration,m.level,m.winner_sets_won,m.loser_sets_won,t.name as t_name,lp.first_name ||' '||lp.last_name as loser_name
from players as p
join single_match as s on p.id = s.winner_id
join matches as m on m.match_id = s.mid
join players as lp on lp.id = s.losers_id
join tournament as t on m.t_id = t.tournament_id and m.year = t.start_year
where p.id = {}
order by m.year DESC, m.t_id ASC
limit 1;""".format(pid))

    result = cursor.first()
    print(result)
    if result is None:
        print("Whoops, sorry we do not have him in the database yet.")
        return redirect("/")

    last_name = result['last_name']
    first_name = result['first_name']
    birthday = result['birthday']
    height = result['height']
    weight = result['weight']
    nation = result['nationality']
    turned_pro = result['start_pro']
    bioinfo = {"last_name": last_name, "first_name": first_name, 'birthday': birthday, "height": height,
               "weight": weight,
               "nation": nation, "turned_pro": turned_pro}

    m_duraion = result['duration']
    m_level = result['level']
    m_losername = result['loser_name']
    m_winner_sets = result['winner_sets_won']
    m_loser_sets = result['loser_sets_won']
    t_name = result['t_name']

    recent = {'duration': m_duraion, 'level': m_level, "loser": m_losername,
              "score": str(m_winner_sets) + '-' + str(m_loser_sets),
              "name": t_name}
    cursor.close()

    # history data
    cmd = """
    SELECT 
date,score
FROM players 
INNER JOIN history_score ON players.id = history_score.pid WHERE history_score.pid = 
{} ORDER BY date DESC LIMIT 20;""".format(pid)
    cursor = g.conn.execute(cmd)
    history_df = []
    for result in cursor:
        history_df.append(result)
    df = pd.DataFrame(history_df, columns=['date', 'score'])
    print(df.dtypes)
    df['date'] = df['date'].astype(str)
    print(df.head())
    print(df.shape)

    min_score, max_score = df['score'].min(), df['score'].max()
    print(min_score, max_score)
    chart_data = df.to_dict(orient='records')
    print(chart_data)
    history_data = {'chart_data': chart_data}

    print(history_data)
    cursor.close()

    # title and champion
    title = {'Grand_Slams':0,'ATP_Masters':0}
    cmd = """SELECT DISTINCT COUNT(tournament_id) as count_gs FROM tournament 
    INNER JOIN players ON tournament.singer_winner_id = players.id 
    WHERE tournament.series_id = 1 and players.id = {} """.format(pid)
    cursor = g.conn.execute(cmd)
    result = cursor.first()
    title['Grand_Slams'] = result['count_gs']
    cursor.close()

    cmd = """SELECT DISTINCT COUNT(tournament_id) as count_master FROM tournament 
    INNER JOIN players ON tournament.singer_winner_id = players.id 
    WHERE tournament.series_id = 2 and players.id = {}""".format(pid)
    cursor = g.conn.execute(cmd)
    result = cursor.first()
    title['ATP_Masters'] = result['count_master']
    cursor.close()

    cmd = """
with tmp as
(select pid,max(date) from history_score group by pid),

tmp1 as (
select tmp.pid,first_name||' '||last_name as name ,tmp.max,score,rank() over (order by score DESC) from history_score, tmp, players
where history_score.pid = tmp.pid
and tmp.pid = players.id
and history_score.date = tmp.max)

select name, rank from tmp1 where pid = {}""".format(pid)
    cursor = g.conn.execute(cmd)
    result = cursor.first()
    recent_rank = result['rank']

    return render_template(
        'player.html',
        title=pid,
        bioinfo=bioinfo,
        recent=recent,
        history_data=history_data,
        min_score=min_score,
        max_score=max_score,
        titles = title,rank = recent_rank)


@app.route("/ranking")
def ranking():
    sql_query = """with tmp as
(select pid,max(date) from history_score group by pid)
select tmp.pid as id,first_name||' '||last_name as name ,tmp.max,score,rank() over (order by score DESC) from history_score, tmp, players
where history_score.pid = tmp.pid
and tmp.pid = players.id
and history_score.date = tmp.max
limit 10;"""
    cursor = g.conn.execute(sql_query)

    # find the top 10 players on the ranking board
    top_10 = []
    for result in cursor:
        player = {'pid': result['id'], 'name': result['name'], 'score': result['score'], 'rank': result['rank']}
        top_10.append(player)

    cursor.close()
    return render_template(
        'ranking.html',
        title="ranking",
        top_10=top_10)


@app.route("/ranking/querydate", methods=['POST'])
def ranking_week():
    print(request.form)
    week = request.form['name']
    print(week)
    print(type(week))
    week = "\'" + week + "\'"
    print(week)

    sql_query = """with tmp as
(select pid,max(date) from history_score where date < {} group by pid)
select first_name||' '||last_name as name ,tmp.max,score,rank() over (order by score DESC) from history_score, tmp, players
where history_score.pid = tmp.pid
and tmp.pid = players.id
and history_score.date = tmp.max
limit 10;""".format(week)

    cursor = g.conn.execute(sql_query)

    # find the top 10 players on the ranking board
    top_10 = []
    for result in cursor:
        player = {'name': result['name'],
                  'score': result['score'], 'rank': result['rank']}
        top_10.append(player)

    cursor.close()
    return render_template(
        'ranking.html',
        title="ranking",
        top_10=top_10, week=week)


if __name__ == "__main__":
    import click


    @click.command()
    @click.option('--debug', is_flag=True)
    @click.option('--threaded', is_flag=True)
    @click.argument('HOST', default='0.0.0.0')
    @click.argument('PORT', default=8111, type=int)
    def run(debug, threaded, host, port):
        """
    This function handles command line parameters.
    Run the server using

        python server.py

    Show the help text using

        python server.py --help

    """

        HOST, PORT = host, port
        print("running on %s:%d" % (HOST, PORT))
        app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


    run()
