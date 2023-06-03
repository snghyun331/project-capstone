from elasticsearch import Elasticsearch, helpers
import pandas as pd
# import os
# import sys 
# sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import updates.daily_aov as aov
import search.get_date as GetDate

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

    return 0




#main start
#when first setting, existing date insert


#day = set_date(2021, 9, 15)
#aov_df = aov.AOV(day, day)
#insert_aov(aov_df)



def do_aov_insert():
    sold_days = GetDate.get_all_date()

    for sold_day in sold_days:
        day_time = GetDate.parse_str_to_date(sold_day)
        aov_df = aov.AOV(day_time, day_time)
        ret = insert_aov(aov_df)

        if (ret == 0) : print(f"{sold_day} insert success")

# sold_days = GetDate.get_all_date()
# for sold_day in sold_days:
#     time = GetDate.parse_str_to_date(sold_day)
#     print(f"{type(time)} type .... time : {time}")

do_aov_insert()

print("test success")