# coding:utf-8
import os
import time
from sqlalchemy import *
import pandas as pd
from sqlalchemy.pool import NullPool
import numpy as np
from datetime import datetime
from tqdm import tqdm
# 与database建立连接
DB_USER = "ll3238"
DB_PASSWORD = "pcuuGKCTf1"

DB_SERVER = "w4111.cisxo09blonu.us-east-1.rds.amazonaws.com"

DATABASEURI = "postgresql://"+DB_USER+":"+DB_PASSWORD+"@"+DB_SERVER+"/w4111"


engine = create_engine(DATABASEURI)
conn = engine.connect()

# 用pandas读入数据
df = pd.read_csv('/Users/raleighliu/Desktop/4111 DB/Tables_to_import/matches.csv')
df_columns = list(df)
columns = ",".join(df_columns)

print(df.shape)

# iteration each row to insert into database
for index,row in tqdm(df.iterrows()):
    print(index)
    match_id = row['match_id']
    # print(match_id)
    t_id = row['t_id']
    year = row['year']
    duration = row['duration']
    level = row['level']
    winner_sets_won = row['winner_sets_won']
    loser_sets_won = row['loser_sets_won']
    winner_games_won = row['winner_games_won']
    loser_games_won = row['loser_games _won']

    loser_aces = row['loser_aces']
    loser_double_faults = row['loser_double_faults']
    loser_first_serves_in = row['loser_first_serves_in']
    loser_first_serves_total = row['loser_first_serves_total']
    loser_first_serve_points_won = row['loser_first_serve_points_won']
    loser_first_serve_points_total = row['loser_first_serve_points_total']
    loser_second_serve_points_won = row['loser_second_serve_points_won']
    loser_second_serve_points_total = row['loser_second_serve_points_total']
    loser_break_points_saved = row['loser_break_points_saved']
    loser_break_points_serve_total = row['loser_break_points_serve_total']
    loser_service_points_won = row['loser_service_points_won']
    loser_service_points_total = row['loser_service_points_total']
    loser_first_serve_return_won = row['loser_first_serve_return_won']
    loser_first_serve_return_total = row['loser_first_serve_return_total']
    loser_second_serve_return_won = row['loser_second_serve_return_won']
    loser_break_points_converted = row['loser_break_points_converted']
    loser_second_serve_return_total = row['loser_second_serve_return_total']
    loser_break_points_return_total = row['loser_break_points_return_total']
    loser_service_games_played = row['loser_service_games_played']
    loser_return_games_played = row['loser_return_games_played']
    loser_return_points_won = row['loser_return_points_won']
    loser_return_points_total = row['loser_return_points_total']
    loser_total_points_won = row['loser_total_points_won']
    loser_total_points_total = row['loser_total_points_total']

    winner_aces = row['winner_aces']
    winner_double_faults = row['winner_double_faults']
    winner_first_serves_in = row['winner_first_serves_in']
    winner_first_serves_total = row['winner_first_serves_total']
    winner_first_serve_points_won = row['winner_first_serve_points_won']
    winner_first_serve_points_total = row['winner_first_serve_points_total']
    winner_second_serve_points_won = row['winner_second_serve_points_won']
    winner_second_serve_points_total = row['winner_second_serve_points_total']
    winner_break_points_saved = row['winner_break_points_saved']
    winner_break_points_serve_total = row['winner_break_points_serve_total']
    winner_service_points_won = row['winner_service_points_won']
    winner_service_points_total = row['winner_service_points_total']
    winner_first_serve_return_won = row['winner_first_serve_return_won']
    winner_first_serve_return_total = row['winner_first_serve_return_total']
    winner_second_serve_return_won = row['winner_second_serve_return_won']
    winner_break_points_converted = row['winner_break_points_converted']
    winner_second_serve_return_total = row['winner_second_serve_return_total']
    winner_break_points_return_total = row['winner_break_points_return_total']
    winner_service_games_played = row['winner_service_games_played']
    winner_return_games_played = row['winner_return_games_played']
    winner_return_points_won = row['winner_return_points_won']
    winner_return_points_total = row['winner_return_points_total']
    winner_total_points_won = row['winner_total_points_won']
    winner_total_points_total = row['winner_total_points_total']

    cmd = """INSERT INTO matches VALUES (\'{}\',{},{},{},\'{}\',{},{},{},{},
    {},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},
    {},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}""".format(
        match_id,t_id, year, duration,level, winner_sets_won,loser_sets_won,winner_games_won,loser_games_won,
        winner_aces, winner_double_faults,
        winner_first_serves_in, winner_first_serves_total,winner_first_serve_points_won, winner_first_serve_points_total,
        winner_second_serve_points_won,winner_second_serve_points_total,
        winner_break_points_saved, winner_break_points_serve_total,
        winner_service_points_won, winner_service_points_total,
        winner_first_serve_return_won,winner_first_serve_return_total,
        winner_second_serve_return_won, winner_second_serve_return_total,
        winner_break_points_converted, winner_break_points_return_total,
        winner_service_games_played,winner_return_games_played,
        winner_return_points_won, winner_return_points_total,
        winner_total_points_won,winner_total_points_total,

        loser_aces, loser_double_faults,
        loser_first_serves_in, loser_first_serves_total, loser_first_serve_points_won,loser_first_serve_points_total,
        loser_second_serve_points_won, loser_second_serve_points_total,
        loser_break_points_saved, loser_break_points_serve_total,
        loser_service_points_won, loser_service_points_total,
        loser_first_serve_return_won, loser_first_serve_return_total,
        loser_second_serve_return_won, loser_second_serve_return_total,
        loser_break_points_converted, loser_break_points_return_total,
        loser_service_games_played, loser_return_games_played,
        loser_return_points_won, loser_return_points_total,
        loser_total_points_won, loser_total_points_total,
    )

    # cmd = 'INSERT INTO players VALUES (\'{}\',\'{}\',\'{}\',\'{}\',{},{},\'{}\',\'{}\',{})'\
    #     .format(id,last_name,first_name,birthday,height,weight, Nationality,play_type,start_pro)
    # try:
    #     conn.execute(cmd)
    #     print("success!")
    # except Exception as e:
    #     print(Exception)
    #     pass
conn.close()