from elasticsearch import Elasticsearch, helpers
from datetime import date, timedelta
import pandas as pd

import AOV as aov

#at end of day this program will be executed
def set_yesterday():
    today = date.today()
    yesterday = today - timedelta(days=1)

    return yesterday

def insert_aov(aov_df):
    es = Elasticsearch(
    hosts='https://118.67.134.52:9200',
    http_auth=("elastic", "elastic"),   
    verify_certs= False,
    http_compress= False
    )

    data_row = []

    for row in aov_df.itertuples():
        data = {
            "_index" : "platform_sales_per_price",
            "_source" : {
                "store_id": row.store_id,
                "total_sale": row.total_sale,
                "num_customer": row.num_customer,
                "unit_price": row.unit_price,
                "date" : row.date
            }
        }

        data_row.append(data)

        if len(data_row) >= 100 : 
            try:
                helpers.bulk(es, data_row)
            except helpers.BulkIndexError as e:
                for error in e.errors:
                    print(error)
            data_row = []

    if data_row : 
        helpers.bulk(es, data_row)




#main start
#day = set_yesterday()
#aov_df = aov.AOV(day, day)

print("test success")