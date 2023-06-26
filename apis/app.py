from flask import Flask, jsonify, request
from elasticsearch import helpers, Elasticsearch
from dateutil import parser
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')
# import os
# import sys 
# sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

es = Elasticsearch(
    hosts='https://118.67.134.52:9200',
    http_auth=("elastic", "elastic"),   
    verify_certs= False,
    http_compress= False
    )


app = Flask(__name__)


@app.route('/')
def home():
    return "엘라스틱 서치를 플라스크로 성능 향상 시키기"


# request parameter에서 date 값을 받아서 해당 범위의 객단가 정보 가져오기
@app.route('/search-unitprice', methods = ['GET'])
def search():
    date = request.args.get('date')
    # url 예시: http://localhost:5000/search-unitprice?date=20230501
    year = date[:4]
    month = date[4:6]
    day = date[6:]

    index = "platform_sales_per_price"
    body = {"query": {"match_all": {}}}
    res = es.search(index = index, scroll = '1m', size = 10000, body = body)
    res_hits = res["hits"]["hits"]
    scroll_id = res['_scroll_id']
    
    new_docs = []
    while len(res_hits) > 0:
        for res_hit in res_hits:  # res_hits[0], res_hits[1]....
            docs = res_hit['_source']
            store_id = docs['store_id']
            total_sale = docs['total_sale']
            num_customer = docs['num_customer']
            unit_price = docs['unit_price']
            date = docs['date']
        
            info = {
                'store_id': store_id,
                'date': date,
                'num_customer': num_customer,
                'total_sale': total_sale,
                'unit_price': unit_price
            }
            if date == f"{year}-{month}-{day}":
                new_docs.append(info)
            
        res = es.scroll(scroll_id = scroll_id, scroll = '1m')   
        res_hits = res['hits']['hits']
    
    return jsonify(new_docs) 



# 특정 가게의 일주일 평균 객단가를 가져오기
@app.route('/search-weekaov',methods = ['GET'])
def Week_AOV(): 
    storeId = request.args.get('store_id')
    # url 예시: http://localhost:5000/search-weekaov?store_id=50
    new_docs = []
    index = 'platform_sales_week_per_price' 
    body = {"query": {"match_all": {}}}
    res = es.search(index = index, body = body, size = 10000)
    res_hits = res["hits"]["hits"]
    for res_hit in res_hits:  # res_hits[0], res_hits[1]....
        docs = res_hit['_source']
        store_id = docs['store_id']
        start_date = docs['start_date']
        end_date = docs['end_date']
        week_unit_price = docs['week_unit_price']
        info = {
                'store_id': store_id,
                'start_date': start_date,
                'end_date': end_date,
                'week_unit_price': week_unit_price,
            }
        if store_id == int(storeId):
            new_docs.append(info)
        else:
            pass
    
    return jsonify(new_docs) 


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 3000)