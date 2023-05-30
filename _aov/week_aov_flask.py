from flask import Flask, jsonify, request
from elasticsearch import Elasticsearch
from dateutil import parser
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

@app.route('/')
def home():
    return "엘라스틱 서치를 플라스크로 성능 향상 시키기"

@app.route('/week_AOV')
def Week_AOV(): 
    es = Elasticsearch(
    hosts='https://118.67.134.52:9200',
    http_auth=("elastic", "elastic"),   
    verify_certs= False,
    http_compress= False
    )
    
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


if __name__ == '__main__':
    app.run(debug=False)