from flask import Blueprint, jsonify, request
from elasticsearch import Elasticsearch
from dateutil import parser

class Conn:
    def __init__(self):
        self.es = Elasticsearch(
            hosts='https://118.67.134.52:9200',
            http_auth=("elastic", "elastic"),
            verify_certs= False,
            http_compress= False
        )

conn = Conn()
elastic_api = Blueprint("elastic_api", __name__)


@elastic_api.route('/')
def home():
    return "엘라스틱 서치를 플라스크로 성능 향상 시키기"

# request parameter에서 start_date, end_date 값을 받아서 해당 범위의 객단가 정보 가져오기
@elastic_api.route('/search-unitprice', methods = ['GET'])
def search():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    start_year = start_date[:4]
    start_month = start_date[4:6]
    start_day = start_date[6:]
    end_year = end_date[:4]
    end_month = end_date[4:6]
    end_day = end_date[6:]
    
    es = conn.Conn()
    index = "platform_sales_per_price"
    body = {"query":
                {"range":
                    {"sold_at": 
                        {
                        "gt":parser.parse(f"{start_year}-{start_month}-{start_day}T00:00:00+00:00"), 
                        "lt":parser.parse(f"{end_year}-{end_month}-{end_day}T23:59:59+00:00")
                        }
                    }
                }
        }
    
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
            
            new_docs.append(info)
            
        res = es.scroll(scroll_id = scroll_id, scroll = '1m')   
        res_hits = res['hits']['hits']
    
    return jsonify(new_docs) 
#     output: [ 
#                 {'store_id':12, 'date': 2020-01-01...},
#                 {'store_id':13, 'date': 2020..}  
#             ]


# 일주일 평균 객단가를 가져오기
@elastic_api.route('/search-weekaov')
def Week_AOV(): 
    es = conn.Conn()
    
    index = 'platform_sales_week_per_price' 
    body = {"query": {"match_all": {}}}
    res = es.search(index = index, body = body, size = 10000)
    res_hits = res["hits"]["hits"]
    docs = res_hits['_source']
    store_id = docs['store_id']
    start_date = docs['start_date']
    end_date = docs['end_date']
    week_unit_price = docs['week_unit_price']
        
    return  f"""
    <h4>store_id: {store_id}</h4>
    <h4>start_date: {start_date}</h4>
    <h4>end_date: {end_date}</h4>
    <h4>week_unit_price: {week_unit_price}</h4>
    """