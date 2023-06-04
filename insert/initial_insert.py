import os
import sys 
import pymysql.cursors
from dateutil import parser
from elasticsearch import helpers

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import elastic.conn as conn
import search.get_date as getdate

def insert_sale(es, db, start_date, end_date):
    try: 
        with db.cursor() as cursor:
            sql = f"SELECT  * FROM platform_sales WHERE sold_at >= {start_date} and sold_at <= {end_date} "
            sql = "SELECT  * FROM platform_sales"

            cursor.execute(sql)

            #send buffer
            data_row = []

            # when data count 100, send to elastic
            for row in cursor: 
                data = {
                    "_index": "platform_sales",
                    "_source": {
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

            #send sale data to server
            if len(data_row) >= 100: 
                try:
                    helpers.bulk(es, data_row)
                except helpers.BulkIndexError as e:
                    for error in e.errors:
                        print(error)
                data_row = []


        #send rest data
        if data_row: 
            helpers.bulk(es, data_row)

    finally:
        db.close()


#execute start
# initialize 
con = conn.Conn()
es = con.es
db = con.db


#set date
max_day_sql = "SELECT DATE_FORMAT(MAX(sold_at), '%Y%m%d') as max_day FROM platform_sales"
min_day_sql = "SELECT DATE_FORMAT(MIN(sold_at), '%Y%m%d') as min_day FROM platform_sales"
max_day = ()
min_day = ()

try:
    with db.cursor() as cursor:
        cursor.execute(max_day_sql)
        max_day = cursor.fetchall()
        cursor.execute(min_day_sql)
        min_day = cursor.fetchall() 
finally:
    print(f"insert data from {min_day[0]['min_day']} to {max_day[0]['max_day']}")

#set date
start_date = min_day[0]['min_day']
end_date = max_day[0]['max_day']

#get date information
start_year = start_date[:4]
start_month = start_date[4:6]
start_day = start_date[6:]
end_year = end_date[:4]
end_month = end_date[4:6]
end_day = end_date[6:]

#date formating
start = getdate.format_date(start_year, start_month, start_day, 0, 0, 0)
end = getdate.format_date(end_year, end_month, end_day, 23, 59, 59)

#main execute
insert_sale(es, db, start, end)

#end
print("from database, transport data to elasticsearch successful")