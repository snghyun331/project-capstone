from elasticsearch import Elasticsearch 
from dateutil import parser
from datetime import timedelta, date
import pandas as pd
# import os
# import sys 
# sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# import elastic.conn as conn

import conn

# 조회하는 데이터의 날짜의 1주일치 데이터 가져와서 객단가 평균 구하기 
def make_week_AOV(date, store_id):
    es = conn.Conn()
    index = 'platform_sales_per_price'
    body = {
        "size": 10000,
        "query": {
            "range": {
                "date": {
                    "gte": parser.parse(f"{date - timedelta(days=7)}"),
                    "lte": parser.parse(f"{date - timedelta(days=1)}")
                }
            }
        }
    }

    total_sale = []
    res = es.search(index=index, body=body)
    res_hits = res["hits"]["hits"]
    for arr in res_hits:
        res_source = dict(arr)
        res_store_id = res_source["_source"]["store_id"]
        if res_store_id == store_id:
            res_unit_price = res_source["_source"]["total_sale"]
            total_sale.append(res_unit_price)

    num_customer = []
    res = es.search(index=index, body=body)
    res_hits = res["hits"]["hits"]
    for arr in res_hits:
        res_source = dict(arr)
        res_store_id = res_source["_source"]["store_id"]
        if res_store_id == store_id:
            res_unit_price = res_source["_source"]["num_customer"]
            num_customer.append(res_unit_price)

    df = pd.DataFrame(columns=["store_id", "start_date", "end_date", "week_unit_price"])

    try:
        week_aov = int(sum(total_sale) / sum(num_customer))
        start_date = date - timedelta(days=7)
        end_date = date - timedelta(days=1)

        data = {
            "store_id": store_id,
            "start_date": start_date,
            "end_date": end_date,
            "week_unit_price": week_aov
        }

        df = df.append(data, ignore_index=True)
    except:
        pass

    return df


def Week_AOV(start_date, end_date):
    start_year = start_date.year
    start_month = start_date.month
    start_day = start_date.day

    end_year = end_date.year
    end_month = end_date.month
    end_day = end_date.day

    es = conn.Conn()

    index = 'platform_sales_per_price'
    body = {
        "size": 10000,
        "query": {
            "range": {
                "date": {
                    "gte": parser.parse(f"{start_year}-{start_month}-{start_day}"),
                    "lte": parser.parse(f"{end_year}-{end_month}-{end_day}")
                }
            }
        },
        "sort": [
            {"date": {"order": "asc"}}
        ]
    }

    res = es.search(index=index, body=body)
    res_hits = res["hits"]["hits"]

    current_date = start_date
    result_df = pd.DataFrame(columns=["store_id", "start_date", "end_date", "week_unit_price"])

    while current_date <= end_date:
        temp = []
        store_id = []

        for arr in res_hits:
            res_source = dict(arr)
            res_store_id = res_source["_source"]["store_id"]
            res_date = res_source["_source"]["date"]
            if res_date == str(current_date):
                temp.append(res_store_id)

        for value in temp:
            if value not in store_id:
                store_id.append(value)

        for value in store_id:
            df = make_week_AOV(current_date, value)
            result_df = pd.concat([result_df, df])

        current_date += timedelta(days=1)

    return result_df


#start_date = date(2021, 12, 14)
#end_date = date(2021, 12, 20)
#temp = Week_AOV(start_date, end_date)

