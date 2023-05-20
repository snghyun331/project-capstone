from elasticsearch import Elasticsearch
from elasticsearch import helpers
from flask import Flask, jsonify, request
from datetime import datetime
from dateutil import parser

es = Elasticsearch("https://118.67.134.52:9200",
                   http_auth=("elastic", "elastic"),
                   verify_certs= False,
                   http_compress= False)

app = Flask(__name__)

@app.route('/')

@app.route('/home')
def home():
    return "엘라스틱 서치를 플라스크로 성능 향상 시키기"

@app.route('/search', methods = ['GET'])
def search():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    # url 예시: http://localhost:5000/search?start_date=20230501&end_date=20230531
    
    start_year = start_date[:4]
    start_month = start_date[4:6]
    start_day = start_date[6:]
    end_year = end_date[:4]
    end_month = end_date[4:6]
    end_day = end_date[6:]
    
    
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
    
if __name__ == '__main__':
    app.run(debug=False)