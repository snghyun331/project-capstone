# project-capstone

# [실행순서] 

### conn.py 
 - 기능 : elasticsearch의 연결

### aov_compare.py
 - 기능 : 데이터의 이상치 검사 
 - 함수 : compare(card_number, amount_sale, store_id, start_date, end_date)
 - 조건 : 주간 객단가의 2배보다 크면서, 데이터의 card_number가 같은 데이터가 amount_sale가 3번 이상 같은 경우 이상치로 간주.

### es.connection.py 
  1. 기능 : DB에서 ELK로 데이터를 이동
  2. 함수 : insert_sale(start_date, end_date)
  3. 전개 :
 - es = conn.Conn() : 'conn.py' 사용자 정의 모듈로 elasticsearch와 연결 
 - DB에 있는 데이터를 pymysql 라이브러리로 조회 후 'platform_sales' 인덱스의 mappings에 맞게 데이터 지정, data_row 리스트에 추가.
 - cmp.compare() : 'aov_compare.py' 사용자 정의 모듈로 이상치이면 fraud_data 리스트에도 추가.
 - 만약 data_row의 길이가 100 이상이면 데이터를 'platform_sales'인덱스에 추가하고 data_row는 초기화.
 - fraud_data의 길이가 100 이상이면 'platform_fraud_sales' 인덱스에 데이터 추가하고 fraud_data는 초기화.
 - DB에 있는 데이터를 platform_sales 인덱스에 추가 
 - DB에서 데이터를 모두 받아온 후 data_row와 fraud_data에 데이터가 존재한다면 각각의 인덱스에 추가.
  
### daily_aov.py 
  1. 기능 : 일일 객단가 계산
  2. 함수 : make_AOV(year, month, day), AOV(start_date, end_date)
  3. 전개 : 
 - make_AOV() 함수
    * 해당 날짜에 존재하는 'platform_sales'의 데이터를 가져와 일일 객단가를 구하기 위한 함수
    * 객단가 = (가게의 총 결제 금액) / (가게의 손님의 수) 
    * 'platform_sales'에서 해당 날짜에 결제된(sold_at) 데이터를 모두 가져온다. 
    * 가져온 데이터로 해당일에 결제된 각각의 가게(store_id)의 일일 객단가를 구하기 위해 store_id 리스트를 만들어 중복이 되지 않게 저장한다. 
    * 해당일에 가게별로 결제한 손님의 수를 구하기 위해 가게(store_id)와 카드 번호(card_number)를 키:값으로 하여 store_id가 같은 값의 갯수를 구하여                         num_customer 딕셔너리에 store_id, len(고객수)를 키:값으로 저장.
    * 가게의 총 결제 금액도 필요하므로, store_id와 가게별 amount_sale의 합계를 키:값으로 정해 total_sales 딕셔너리에 저장
    * store_id, num_customer 딕셔너리, total_sales 딕셔너리를 이용하여 가게별 객단가(aov)를 구해 store_id와 aov를 키:값으로 unit_price 딕셔너리에 저장. 
    * data 딕셔너리를 'platform_sales_per_price' 인덱스와 필드를 같게 만들어 store_id, total_sale, num_customer, unit_price값 저장.
    * data 딕셔너리를 DataFrame으로 만들고(df), 해당 날짜의 데이터를 넣는 'date' 필드 추가. 
    * 만든 df은 AOV에 리턴.
 - AOV() 함수 
    * 일일 객단가를 구하고 싶은 시작 날짜(start_date)와 끝 날짜(end_date)를 인자로 한다.
    * current_date는 start_date에서 end_date까지의 날짜 데이터를 얻기 위한 변수
    * 이후에 'platform_sales_per_price' 인덱스에 저장하기 편하게 하도록 result_df 데이터프레임을 만들어 둔다.
    * current_date를 년, 월, 일로 나눠 make_AOV()함수의 인자로 사용, 리턴값은 df에 저장 
    * make_AOV() 함수를 실행하고 리턴받은 값 df는 result_df와 합친다. 
    * current_date를 하루 증가시켜 end_date가 될때까지 make_AOV() 실행하고 df는 result_df와 합친다. 
    * 최종적으로 result_df는 start_date부터 end_date까지 일일 객단가를 구한 DataFrame이 된다. 
          
3. initial_aov.py 
  - 기능 : daily_aov.py 에서 계산된 값을 ELK로 이동 

4. week_aov.py 
  - 기능 : 주간 객단가 계산 

5. 
