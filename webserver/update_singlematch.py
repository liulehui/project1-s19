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
df = pd.read_csv('/Users/raleighliu/Desktop/4111 DB/Tables_to_import/single_match.csv')
df_columns = list(df)
columns = ",".join(df_columns)

print(df.shape)
exception = 0
# iteration each row to insert into database
for index,row in tqdm(df.iterrows(),total=df.shape[0]):
    # print(index)
    mid = row['mid']
    # print(match_id)
    winner_id = row['winner_id']
    losers_id = row['losers_id']

    cmd = """INSERT INTO single_match VALUES (\'{}\',\'{}\',\'{}\')""".format(
        mid, winner_id,losers_id
    )

    try:
        conn.execute(cmd)
        print("success!")
    except Exception as e:
        exception += 1
        print(Exception)
        pass
print(exception)
conn.close()