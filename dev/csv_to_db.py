import os
import sys 
import pandas as pd
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import elastic.conn as conn
import search.get_date as getdate

con = conn.Conn()
db = con.db
cursor = db.cursor()


def insert_csv(num_csv):

    # csv 
    df = pd.read_csv("D:\platform_sales\platform_sales_%d.csv" % num_csv)
    df = df.replace(np.nan, None) # nan값 None으로 치환.

    for row in range(0,len(df) - 1):
        data = df.iloc[row]

        #check date
        #this case, more than 2022-05-31 sold_at date insert
        ins_date = getdate.format_date(2022, 5, 31, 0, 0, 0)
        row_date = getdate.format_date(data[12][:4], data[12][5:7], data[12][8:10], data[12][11:13], data[12][14:16], data[12][17:19])

        if ins_date > row_date : 
            continue

        #set insert data
        id = data[0]
        created = data[1]
        modified = data[2]
        remark = data[3]
        num_approval = data[4]
        card_company = data[5]
        card_category = data[6]
        card_number = data[7]
        amount_sale = data[8]
        amount_fee = data[9]
        amount_deposit = data[10]
        is_canceled = int(data[11])
        sold_at = data[12]
        will_deposited_at = data[13]
        raw_data = data[14]
        platform = data[15]
        daily_sale = data[16]
        store_id = data[17]
        result_code = data[18]
        result_msg = data[19]
        extra_payment_id = data[20]
        detail_status = data[21]
        processing_status = data[22]
        
        insert_query = """insert into platform_sales values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        try:
            cursor.execute(insert_query, (id, created, modified, remark, num_approval, card_company, card_category, card_number, amount_sale, amount_fee, amount_deposit, is_canceled, sold_at, will_deposited_at, raw_data, platform, daily_sale, store_id, result_code, result_msg, extra_payment_id, detail_status, processing_status))
        except Exception as e:
            print(f"An error occurred: {e}")
        #print(f"sold_at = {data[12]}, type = {type(data[12])}")
        

#execute area
insert_csv(49)

db.commit()
db.close()    