from elasticsearch import Elasticsearch

class Conn:
    def __init__(self):
        self.es = Elasticsearch(
            hosts='https://118.67.134.52:9200',
            http_auth=("elastic", "elastic"),   
            verify_certs= False,
            http_compress= False
        )

