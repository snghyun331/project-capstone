# data to es

from elasticsearch import Elasticsearch, helpers
import pymysql.cursors
from dateutil import parser
import datetime

import es_connection as es_con

import elastic.conn as conn

es = conn.Conn()

es.ping()


connection = pymysql.connect(
    host = 'localhost',
    port = 3306,
    user = 'root',
    password = '12345',
    db='_earlypay',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)


#from insert program, execute cycle program
#cycle : 6 hour
def insert_sales_cycle():
    exe_time = datetime.datetime.now()
    year = exe_time.year
    month = exe_time.month
    day = exe_time.day
    hour = exe_time.hour
    minute = exe_time.minute
    second = exe_time.second

    start_time = exe_time + datetime.timedelta(hours=-6)
    s_year = start_time.year
    s_month = start_time.month
    s_day = start_time.day
    s_hour = start_time.hour
    s_minute = start_time.minute
    s_second = start_time.second

    start = es_con.format_date(s_year, s_month, s_day, s_hour, s_minute, s_second)
    end = es_con.format_date(year, month, day, hour, minute, second)
    print(start)
    print(end)

    es_con.insert_sale(start, end)

#insert_sales_cycle()

print("insert end")