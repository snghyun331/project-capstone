from elasticsearch import Elasticsearch, helpers
from datetime import date, timedelta
from dateutil import parser
import pandas as pd

import AOV as aov


def set_date(year, month, day):
    return parser.parse(f"{year}-{month}-{day}T00:00:00+00:00")


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
#when first setting, existing date insert

#day = set_date(2021, 9, 15)
#aov_df = aov.AOV(day, day)
#insert_aov(aov_df)


print("test success")