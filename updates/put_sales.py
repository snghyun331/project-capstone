import os
import sys 
from dateutil import parser
from elasticsearch import helpers
from datetime import timedelta

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import elastic.conn as conn
import search.get_date as getdate
import elastic.aov_compare as cmp

def check_insert_sale(es, db, start_date, end_date):
    try: 
        with db.cursor() as cursor:
            sql = f"""SELECT  * 
            FROM platform_sales 
            WHERE sold_at >= '{start_date}' and sold_at <= '{end_date}' """

            print("execute query")
            cursor.execute(sql)

            #send buffer
            data_row = []
            fraud_data = []

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

                #append fraud data
                if not cmp.compare(es, row["card_number"], row["amount_sale"], row["store_id"], row["sold_at"]):
                    print(f"detect fraud data")
                    data['_index'] = "platform_fraud_sales"
                    fraud_data.append(data)
            
                #send sale data to server
                if len(fraud_data) >= 100: 
                    try:
                        helpers.bulk(es, fraud_data)
                    except helpers.BulkIndexError as e:
                        for error in e.errors:
                            print(error)
                    fraud_data = []
            
                #send sale data to server
                if len(data_row) >= 100: 
                    try:
                        helpers.bulk(es, data_row)
                    except helpers.BulkIndexError as e:
                        for error in e.errors:
                            print(error)
                    data_row = []
                print("row end")


            #send rest data
            if data_row: 
                helpers.bulk(es, data_row)
            if fraud_data: 
                helpers.bulk(es, fraud_data)

    finally:
        db.close()


#execute start
# initialize 
con = conn.Conn()
es = con.es
db = con.db

#set date
#exe_time = getdate.get_cycle_term()
#start = exe_time[0]
#end = exe_time[1]

end = getdate.format_date(2022, 5, 31, 12, 0, 0)
start = end - timedelta(hours=6)

print(f"start = {start}, end = {end}")
#main execute
check_insert_sale(es, db, start, end)

#end
print("successful insert cycle end")