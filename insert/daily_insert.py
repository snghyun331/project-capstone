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

    print("daily insert success")



### at server ###
#main start
#when first setting, existing date insert
###
#days = GetDate.get_all_date()
#for day in days:
#    aov_df = aov.AOV(day, day)
#    insert_aov(aov_df)



###
# every day 00:00:00 clock execute this program
###
#day = GetDate.set_yesterday()
#aov_df = aov.AOV(day, day)
#insert_aov(aov_df)



print("daily insert end")