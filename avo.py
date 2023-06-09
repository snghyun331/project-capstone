# 데일리 객단가 구하기 
# 공식 : 일일 총 매출액 / 일일 결제한 총 인원수 
from elasticsearch import Elasticsearch 
from dateutil import parser

def search(year, month, day):
    es = Elasticsearch("http://localhost:9200", http_auth=("elastic", "elastic"))
    
    # ------------------------- 일일 결제 내역 확인 -------------------------
    index = "platform_sales"
    body = {"query":
                {"range":
                    {"sold_at": 
                         {
                             "gt":parser.parse(f"{year}-{month}-{day}T00:00:00+00:00"), 
                             "lt":parser.parse(f"{year}-{month}-{day}T23:59:59+00:00")
                         }
                    }
                }
           }
    
    res = es.search(index = index, body = body)
    
    # ------------------------ 일일 이용 회원 -------------------------------
    temp = []
    client_num = []
    
    res_hits = res["hits"]["hits"]
    for arr in res_hits:
        res_source = dict(arr)
        res_card_number = res_source["_source"]["card_number"]
        temp.append(res_card_number)
    
    for value in temp:
        if value not in client_num:
            client_num.append(value)
    
    total_client_num = len(client_num) # 일일 이용 회원 수
          
    # --------------------- 일일 총 결제 금액 -----------------------------
    amount_sale = []
    
    res_hits = res["hits"]["hits"]
    for arr in res_hits:
        res_source = dict(arr)
        res_amount_sale = res_source["_source"]["amount_sale"]
        amount_sale.append(res_amount_sale)
       
    total_amount_sale = sum(amount_sale) ## 일일 결제 금액 총합
  
    # --------------------- 객단가 ------------------------------------------
    avo = total_amount_sale / total_client_num
    print("일일 이용 회원 수 :", total_client_num, "명",
          "\n일일 총 결제 금액 :", total_amount_sale, "USD", 
          "\n객단가 :", avo, "USD")
    
#search({year}, {month}, {day}) # 년도, 달, 일 입력
