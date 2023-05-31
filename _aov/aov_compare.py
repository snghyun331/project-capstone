from elasticsearch import Elasticsearch 

def compare(unit_price):
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
    week_unit_price = docs["week_unit_price"]
    
    if week_unit_price * 2 < unit_price:   # 일주일 객단가 > insert 데이터 객단가 이면 true 반환
        return True
    else:
        return False
    