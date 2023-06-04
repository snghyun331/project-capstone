from datetime import datetime
from dateutil import parser
from elasticsearch import Elasticsearch

import conn

def compare(card_number, amount_sale, store_id, start_date):
    start_year = start_date.year
    start_month = start_date.month
    start_day = start_date.day
   
    es = conn.Conn()
    
    # 주간 객단가 가져오기 
    index1 = 'platform_sales_week_per_price' 
    body1 = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"store_id": store_id}},
                    {"match": {"start_date": start_date}}
                ]
            }
        }
    }
    res1 = es.search(index=index1, body=body1, size=10000)
   
    # 특정 store_id의 데이터 가져오기 
    index2 = 'platform_sales' 
    body2 = {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"store_id": store_id}},
                        {"range": {
                            "sold_at": {
                                "gte": parser.parse(f"{start_year}-{start_month}-{start_day}T00:00:00+00:00"),
                                "lte": parser.parse(f"{start_year}-{start_month}-{start_day}T23:59:59+00:00")
                            }
                        }}
                    ]
                }
            }
        }
    res2 = es.search(index = index2, body = body2, size = 10000)
    
    # pltform_sales_week_per_price에서 week_unit_price값 가져오기 
    res1_hits = res1["hits"]["hits"]
    res1_source = dict(res1_hits[0])
    week_unit_price = res1_source["_source"]["week_unit_price"]
    
    
    # platform_sales에서 amount_sale값 가져오기
    res2_hits = res2["hits"]["hits"] 
    info = [] # 비교하는 데이터의 card_number가 같은 amount_sale값의 리스트
    for arr in res2_hits:
        res2_source = dict(arr)
        current_card_number = res2_source["_source"]["card_number"] # 현재 es에 저장된 데이터의 card_number들
        if card_number == current_card_number: # 비교하는 데이터와 카드 번호가 같을 경우 리스트에 추가
            info.append(res2_source["_source"]["amount_sale"])
      
    # 가장 최근의 3개의 amount_sale의 값이 모두 같은 값이면 변수 outlier는 true
    count = 0
    outlier = True
    for value in range(-1, -len(info), -1):
        if info[value] == amount_sale:
            count += 1
            if count >= 2:
                outlier = True
        else:
            outlier = False
            break
  
    
    if week_unit_price*2 < amount_sale or outlier == True:
        return True
    else:
        return False
    
# df = compare("5461-11**-****-7537", 32000, 56, "20220202")
# 예시) 카드 번호가 5461-11**-****-7537인 고객이 56번 가게에 32000원씩 3번 이상 결제해서 True가 나옴  






""" 이전 
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
    """
