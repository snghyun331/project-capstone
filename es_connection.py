from elasticsearch import Elasticsearch, helpers
import pymysql.cursors
from dateutil import parser
import datetime

import _aov.aov_compare as cmp

es = Elasticsearch(
    hosts='https://118.67.134.52:9200',
    http_auth=("elastic", "elastic"),   
    verify_certs= False,
    http_compress= False
)

es.ping()


connection = pymysql.connect(
    host = 'localhost',
    port = 3306,
    user = 'root',
    password = '12345',
    db='_earlypay',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

def format_date(year, month, day, hour, minute, second):

    return parser.parse(f"{year}-{month}-{day}T{hour}:{minute}:{second}+00:00")



def insert_sale(start_date, end_date):
    try : 
        with connection.cursor() as cursor:
            sql = f"SELECT  * FROM platform_sales WHERE sold_at >= {start_date} and sold_at <= {end_date} "
            sql = "SELECT  * FROM platform_sales"

            cursor.execute(sql)

            #send buffer
            data_row = []
            fraud_data = []

            # when data count 100, send to elastic
            for row in cursor : 
                data = {
                    "_index" : "platform_sales",
                    "_source" : {
                    "id": row["id"],
                    "created": parser.parse(row["created"]).isoformat(),
                    "modified": parser.parse(row["modified"]).isoformat(),
                    "remark": row["remark"],
                    "num_approval": row["num_approval"],
                    "card_company": row["card_company"],
                    "card_category": row["card_category"],
                    "card_number": row["card_number"],
                    "amount_sale": row["amount_sale"],
                    "amount_fee": row["amount_fee"],
                    "amount_deposit": row["amount_deposit"],
                    "is_canceled": bool(row["is_canceled"]),
                    "sold_at": parser.parse(row["sold_at"]).isoformat(),
                    "will_deposited_at": parser.parse(row["will_deposited_at"]).isoformat(),
                    "raw_data": row["raw_data"],
                    "platform": row["platform"],
                    "daily_sale_id": row["daily_sale_id"],
                    "store_id": row["store_id"],
                    "result_code": row["result_code"],
                    "result_msg": row["result_msg"],
                    "extra_payment_id": row["extra_payment_id"],
                    "detail_status": row["detail_status"],
                    "processing_status": row["processing_status"]
                    }
                }
            #append sale data
            data_row.append(data)

            #check aov and append sale data
            if cmp.compare(row["amount_sale"], row["store_id"], row["sold_at"]):
                fraud_data.append(data)

            #send sale data to server
            if len(data_row) >= 100 : 
                try:
                    helpers.bulk(es, data_row)
                except helpers.BulkIndexError as e:
                    for error in e.errors:
                        print(error)
                data_row = []

            #send fraud data to server
            if len(fraud_data) >= 100 : 
                try:
                    helpers.bulk(es, fraud_data)
                except helpers.BulkIndexError as e:
                    for error in e.errors:
                        print(error)
                fraud_data = []

        #send rest data
        if data_row : 
            helpers.bulk(es, data_row)
        if fraud_data : 
            helpers.bulk(es, fraud_data)

    finally :
        connection.close()


###### existing date dates ######
#start = format_date(2021, 9, 15, 0, 0, 0)
#end = format_date(2022, 5, 31, 23, 59, 59)

#insert_sale(start, end)

print("insert end")