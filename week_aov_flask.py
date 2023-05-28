from flask import Flask, jsonify, request
from elasticsearch import Elasticsearch
from dateutil import parser
import warnings
warnings.filterwarnings('ignore')

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
    
    res = es.search(index = index, body = body, scroll = '1m',size = 10000)
    res_hits = res["hits"]["hits"]
    scroll_id = res['_scroll_id']
    
    while len(res_hits) > 0:
        for arr in res_hits:
            res_source = dict(arr)
            res_store_id = res_source["_source"]["store_id"]
            if res_store_id == store_id: # 해당 id와 store_id가 같은 객단가의 값만 가져옴
                res_unit_price = res_source["_source"]["unit_price"]
                unit_price.append(res_unit_price)
                
        res = es.scroll(scroll_id = scroll_id, scroll = '1m')   
        res_hits = res['hits']['hits']
        
    try:
        week_aov = int(sum(unit_price) / len(unit_price))
        
    except ZeroDivisionError:
        week_aov = "해당 날짜에 결제한 회원이 존재하지 않습니다."
    
    # insert한 데이터 날짜 기준 
    # start_date = date(year, month, day - 7)
    # end_date = date(year, month, day - 1)
    # store_id ## 데이터의 가게 고유 번호 
    return week_aov

app = Flask(__name__)

@app.route('/')
def home():
    return "엘라스틱 서치를 플라스크로 성능 향상 시키기"

# 조회하는 데이터의 날짜의 1주일치 데이터 가져와서 객단가 평균 구하기 
@app.route('/week_AOV/<id>')

# id를 받아서 date값과 store_id값을 추출하여 make_week_aov함수의 인자로 사용
def Week_AOV(id): 
    es = Elasticsearch(
    hosts='https://118.67.134.52:9200',
    http_auth=("elastic", "elastic"),   
    verify_certs= False,
    http_compress= False
    )
    
    index = 'platform_sales' 
    body = {
            "query": { "match" : {"id" : id}}
           }
    res = es.search(index = index, body = body, scroll = '1m',size = 10000)
    res_hits = res["hits"]["hits"]
    scroll_id = res['_scroll_id']
    
    while len(res_hits) > 0:
        for arr in res_hits:
            res_source = dict(arr)
            res_sold_at = res_source["_source"]["sold_at"]

            res_date = parser.parse(res_sold_at).date() # res_sold_at을 날짜만 가져옴
            res_store_id = res_source["_source"]["store_id"] # store_id값 추출
            
        res = es.scroll(scroll_id = scroll_id, scroll = '1m')   
        res_hits = res['hits']['hits']
    return  f"""
    <h1>insert 데이터의 ID: {id}</h1>
    <h4>1주간 객단가 평균: {make_week_AOV(res_date, res_store_id)}</h4>
    """
    
#print(Week_AOV(5555)) 
## platform_sales_per_price 인덱스에서 id가 5555번인 데이터와 store_id가 같은 객단가를 7일(1주)전의 데이터까지 평균낸 값 리턴 
if __name__ == '__main__':
    app.run(debug=False)