# 데일리 객단가 구하기 
# 공식 : 일일 총 매출액 / 일일 결제한 총 인원수 

from dateutil import parser
import pandas as pd
from datetime import date, timedelta


def make_AOV(es, year, month, day):
    
    # ------------------------- 일일 결제 내역 확인 -------------------------
    index = 'platform_sales'
    body = {
            "size": 10000,
            "query":
                    {"range":
                        {"sold_at": 
                            {
                            "gte":parser.parse(f"{year}-{month}-{day}T00:00:00+00:00"), 
                            "lte":parser.parse(f"{year}-{month}-{day}T23:59:59+00:00")
                            }
                        }
                    }
        }
    
    res = es.search(index = index, body = body)
    
    # ------------------------ 가게 -------------------------------
    temp = []
    store_id = []
    
    res_hits = res["hits"]["hits"]
    
    for arr in res_hits:
        res_source = dict(arr)
        res_store_id = res_source["_source"]["store_id"]
        temp.append(res_store_id)
    
    for value in temp:
        if value not in store_id:
            store_id.append(value) # 해당 날짜의 결제한 가게들의 store_id가 저장됨
    
    # ------------------------- 가게별 고객수 ---------------------------        

    
    info = []

    for store in store_id: # 가게별로 고객수 저장...
        for arr in res_hits:
            res_source = dict(arr)
            if store == res_source["_source"]["store_id"]:
                info.append([store, res_source["_source"]["card_number"]])
    
    grouped = {}
    num_customer = {}
    
    for item in info:
        key = item[0]
        if key in grouped:
            grouped[key].append(item)
        else:
            grouped[key] = [item]
    
    for key, values in grouped.items():
        num_customer[key] = len(values)

    # --------------------- 가게별 일일 총 결제 금액 -----------------------------
    amount_sale = []
    total_sales = {}
    
    for store in store_id:
        for arr in res_hits:
            res_source = dict(arr)
            if store == res_source["_source"]["store_id"]:
                res_amount_sale = res_source["_source"]["amount_sale"]
                amount_sale.append(res_amount_sale)     
        total_sales[store] = sum(amount_sale) ## total_sales에 가게별 일일 매출 저장
        amount_sale = []

    # --------------------- 객단가 ------------------------------------------
    
    try:
        unit_price = {} 
        for store_id in num_customer:
            if num_customer[store_id] != 0:
                aov = int(total_sales[store_id] / num_customer[store_id])
                unit_price[store_id] = aov # 가게별 계산된 객단가 값 저장 
            else:
                unit_price[store_id] = 0
    except ZeroDivisionError:
        print("해당 날짜에 결제한 고객이 존재하지 않습니다.")
        
    data = {
        "store_id": list(num_customer.keys()),
        "total_sale": list(total_sales.values()),
        "num_customer": list(num_customer.values()),
        "unit_price": list(unit_price.values())
    }   
    
    df = pd.DataFrame(data)
    df["date"] = date(year, month, day)
    
    return df

def AOV(es, start_date, end_date):
    current_date = start_date
    result_df = pd.DataFrame(columns = ["store_id", "total_sale", "num_customer", "unit_price"])
    
    while current_date <= end_date:
        
        year = current_date.year
        month = current_date.month
        day = current_date.day
        
        df = make_AOV(es, year, month, day)
        result_df = pd.concat([result_df, df])
        
        current_date += timedelta(days=1)

    return result_df

