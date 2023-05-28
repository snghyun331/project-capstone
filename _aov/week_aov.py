from elasticsearch import Elasticsearch 
from dateutil import parser
import datetime
    
# 조회하는 데이터의 날짜의 1주일치 데이터 가져와서 객단가 평균 구하기 
def make_week_AOV(date, store_id):
    
    year = date.year
    month = date.month
    day = date.day
    
    es = Elasticsearch(
    hosts='https://118.67.134.52:9200',
    http_auth=("elastic", "elastic"),   
    verify_certs= False,
    http_compress= False
    )
    
    # ------------------------- 1주일내의 결제 내역 확인 -------------------------
    index = 'platform_sales_per_price' 
    body = {
            "size": 10000,
            "query":
                    {"range":
                        {"date": 
                             {
                                 "gte":parser.parse(f"{year}-{month}-{day - 7}"),
                                 "lte":parser.parse(f"{year}-{month}-{day - 1}")
                             }
                        }
                    }
           }
    
    unit_price = [] # 객단가의 집합
    
    res = es.search(index = index, body = body)
    res_hits = res["hits"]["hits"]
    for arr in res_hits:
        res_source = dict(arr)
        res_store_id = res_source["_source"]["store_id"]
        if res_store_id == store_id: # 해당 id와 store_id가 같은 객단가의 값만 가져옴
            res_unit_price = res_source["_source"]["unit_price"]
            unit_price.append(res_unit_price)
            
    week_aov = int(sum(unit_price) / len(unit_price))
    
    # insert한 데이터 날짜 기준 
    # start_date = date(year, month, day - 7)
    # end_date = date(year, month, day - 1)
    # store_id ## 데이터의 가게 고유 번호 
    data = {
        "store_id": store_id,
        "start_date": datetime.date(year, month, day - 7),
        "end_date": datetime.date(year, month, day - 1),
        "week_unit_price": week_aov
    }   

    es.index(index="platform_sales_week_per_price", doc_type="_doc", body=data)
    print("done")
