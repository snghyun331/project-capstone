from elasticsearch import Elasticsearch
import warnings
from datetime import datetime, date, timedelta
from dateutil import parser
warnings.filterwarnings('ignore')
# import os
# import sys 
# sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import elastic.conn as conn

def format_date(year, month, day, hour, minute, second):

    return parser.parse(f"{year}-{month}-{day}T{hour}:{minute}:{second}+00:00")


def set_date(year, month, day):
    return parser.parse(f"{year}-{month}-{day}T00:00:00+00:00")


#at end of day this program will be executed
def set_yesterday():
    today = date.today()
    yesterday = today - timedelta(days=1)

    return yesterday

#at execute (put_sales.py) 
#required between that time and before 6 hour
def get_cycle_term():
    now = date.now()
    before_6 = now - timedelta(hours=6)

    term = (before_6, now)
    return term

def get_all_date():
    
    con = conn.Conn()
    es = con.es
    
    res = es.search(index = 'platform_sales',scroll = '1m', size = 10000, body={"query": {"match_all": {}}})
    res_hits = res['hits']['hits']
    scroll_id = res['_scroll_id']

    new_docs = []
    while len(res_hits) > 0:
        for res_hit in res_hits:
            docs = res_hit['_source']
            sold_at = docs['sold_at']
            sold_at_date = sold_at[:10]
            new_docs.append(sold_at_date)
            
        res = es.scroll(scroll_id = scroll_id, scroll = '1m')   # # 이전 검색 결과와 동일한 scroll_id를 사용하여 다음 검색 결과를 가져옴
        res_hits = res['hits']['hits']
        
    no_duplicate = list(dict.fromkeys(new_docs))
    return no_duplicate


def parse_str_to_date(str_date):
    try:
        ret_date = datetime.strptime(str_date, '%Y-%m-%d')
        return ret_date
    except ValueError as ve:
        print(f"Value Error : {ve}")

    return set_date(1950, 12, 31)
    

