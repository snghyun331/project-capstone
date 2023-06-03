from datetime import datetime
from dateutil import parser
from elasticsearch import Elasticsearch
import conn

def compare(amount_sale,store_id, start_date, end_date):
    start_year = start_date[:4]
    start_month = start_date[4:6]
    start_day = start_date[6:]
    end_year = end_date[:4]
    end_month = end_date[4:6]
    end_day = end_date[6:]
    
    es = conn.Conn()
    
    index = 'platform_sales_week_per_price' 
    body = {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"store_id": store_id}},
                        {"range": {
                            "sold_at": {
                                "gte": parser.parse(f"{start_year}-{start_month}-{start_day}T00:00:00+00:00"),
                                "lte": parser.parse(f"{end_year}-{end_month}-{end_day}T23:59:59+00:00")
                            }
                        }}
                    ]
                }
            }
        }
    res = es.search(index = index, body = body, size = 10000)
    res_hits = res["hits"]["hits"]
    docs = res_hits['_source']
    week_unit_price = docs["week_unit_price"]
    
    if week_unit_price*2 < amount_sale:
        return True
    else:
        return False
    