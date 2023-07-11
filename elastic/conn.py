from elasticsearch import Elasticsearch
import pymysql.cursors

class Conn:
    def __init__(self):
        self.es = Elasticsearch(
            hosts='https://118.67.134.52:9200',
            http_auth=("elastic", "elastic"),   
            verify_certs= False,
            http_compress= False
        )

        self.db = pymysql.connect(
            host = 'localhost',
            port = 3306,
            user = 'root',
            password = '12345',
            db = '_earlypay',
            charset ='utf8mb4',
            cursorclass = pymysql.cursors.DictCursor
        )

