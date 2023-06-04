import os
import sys 
from elasticsearch import helpers

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import elastic.conn as conn
import search.get_date as getdate
import updates.week_aov as week_aov

def insert_weekly_aov(es, aov_df):
    data_row = []

    for row in aov_df.itertuples():
        data = {
            "_index" : "platform_sales_week_per_price",
            "_source" : {
                "store_id": row.store_id,
                "total_sale": row.total_sale,
                "num_customer": row.num_customer,
                "unit_price": row.unit_price,
                "date" : row.date
            }
        }

        data_row.append(data)

        if len(data_row) >= 100: 
            try:
                helpers.bulk(es, data_row)
            except helpers.BulkIndexError as e:
                for error in e.errors:
                    print(error)
            data_row = []

    if data_row: 
        helpers.bulk(es, data_row)

    print("weekly insert success")


#start 

con = conn.Conn()
es = con.es

#in elasticseartch data, select all days
days = getdate.get_all_date()

#by all days, Calculate aov data and put into index (sales_per_prices)
for day in days:
    aov_df = week_aov.Week_AOV(es, day, day)
    insert_weekly_aov(es, aov_df)